class StageOutputMiddleware(object):

    def __init__(self, pipeline_context, stage_config, stage_uuid, stage_context):
        self._pipeline_context = pipeline_context
        self._stage_config = stage_config
        self._stage_uuid = stage_uuid
        self._stage_context = stage_context

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        result = callback(args, kwargs)
        if self._stage_config.persisted():
            self._pipeline_context.stage_contexts[self._stage_uuid].stage_output = result
        return result
