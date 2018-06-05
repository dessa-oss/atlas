class ContextAwareMiddleware(object):

    def __init__(self, stage_context, stage):
        self._stage_context = stage_context
        self._stage = stage

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        from vcat.context_aware import ContextAware

        if isinstance(self._stage.function, ContextAware):
            self._stage.function.set_context(self._stage_context)

        return callback(args, kwargs)
