class UpstreamResultMiddleware(object):

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        new_args = upstream_result_callback() + list(args)

        return callback(new_args, kwargs)
