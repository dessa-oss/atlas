class UpstreamResultMiddleware(object):

    def __init__(self, stage_context):
        self._stage_context = stage_context

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        upstream_result = upstream_result_callback()
        new_args = [upstream_result] + list(args)

        return callback(new_args, kwargs)
