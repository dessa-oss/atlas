class ArgumentFillerMiddleware(object):
    def __init__(self, stage):
        self._stage = stage

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        new_args, new_kwargs = self._stage.fill_args_and_kwargs(filler_builder, **filler_kwargs)
        return callback(new_args, new_kwargs)
    