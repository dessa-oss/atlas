from vcat.stage import Stage


class StageSmartConstructor(object):

    def __init__(self, pipeline_context):
        self._pipeline_context = pipeline_context

    def make_stage(self, function, *args, **kwargs):
        import uuid
        stage_uuid = uuid.uuid4()
        stage_uuid = str(stage_uuid)
        return Stage(stage_uuid, self._wrapped_function(stage_uuid, function), function, *args, **kwargs)

    def _wrapped_function(self, stage_uuid, function):
        def wrapped(*args, **kwargs):
            import time

            start_time = time.time()
            stage_output = function(*args, **kwargs)
            end_time = time.time()
            if isinstance(stage_output, tuple):
                return_value, result = stage_output
                self._pipeline_context.results[stage_uuid] = result
            else:
                return_value = stage_output
            self._pipeline_context.meta_data[stage_uuid] = {
                "start_time": start_time,
                "end_time": end_time,
                "delta_time": end_time - start_time,
            }
            return return_value
        return wrapped
