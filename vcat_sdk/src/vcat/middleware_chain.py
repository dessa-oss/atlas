class MiddlewareChain(object):

    def __init__(self):
        self._chain = []

    def append_middleware(self, middleware):
        self._chain.append(middleware)

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        return self._call_internal(upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback, 0)

    def _call_internal(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback, middleware_index):
        def recursive_callback(args, kwargs):
            return self._call_internal(upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback, middleware_index + 1)

        def execute_callback(args, kwargs):
            return callback(*args, **kwargs)

        if middleware_index < len(self._chain):
            next_callback = recursive_callback
        else:
            next_callback = execute_callback

        return self._chain[middleware_index].call(upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, next_callback)
