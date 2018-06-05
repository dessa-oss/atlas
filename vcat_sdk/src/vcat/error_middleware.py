class ErrorMiddleware(object):

    def __init__(self, stage_context):
        self._stage_context = stage_context

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        try:
            return callback(args, kwargs)
        except:
            import sys
            self._stage_context.add_error_information(sys.exc_info())
            raise
