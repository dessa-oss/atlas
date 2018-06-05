class ArgumentFillerMiddleware(object):
    def __init__(self, stage):
        self._stage = stage

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        new_args, new_kwargs = filler_builder(*args, **kwargs).fill(**filler_kwargs)
        return callback(new_args, new_kwargs)
    