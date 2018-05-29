from vcat.stage import Stage


class StageSmartConstructor(object):

    def __init__(self, stage_context):
        self._stage_context = stage_context

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
                self._stage_context.stage_log = result
            else:
                return_value = stage_output
            self._stage_context.start_time = start_time
            self._stage_context.end_time = end_time
            self._stage_context.delta_time = end_time - start_time
            return return_value
        return wrapped
