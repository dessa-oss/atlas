class UpstreamResultMiddleware(object):

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        upstream_result = upstream_result_callback()
        new_args = [upstream_result] + list(args)

        return callback(new_args, kwargs)
