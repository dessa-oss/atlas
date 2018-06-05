class RedundantExecutionMiddleware(object):

    def __init__(self):
        self._result = None
        self._has_run = False

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        if self._has_run:
            return self._result
        else:
            self._result = callback(args, kwargs)
            self._has_run = True
            return self._result
