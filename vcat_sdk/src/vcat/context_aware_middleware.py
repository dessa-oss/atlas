class ContextAwareMiddleware(object):

    def __init__(self, stage_context):
        self._stage_context = stage_context

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        # TODO: support context awareness if a ContextAware is provided
        # new_args = [self._stage_context] + list(args)

        return callback(args, kwargs)
