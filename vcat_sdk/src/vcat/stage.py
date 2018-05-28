class Stage(object):

    def __init__(self, uuid, function, metadata_function, *args, **kwargs):
        self.uuid = uuid
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self._metadata_function = metadata_function

    def run(self, previous_results, filler_builder, **filler_kwargs):
        filler = filler_builder(*self.args, **self.kwargs)
        new_args, new_kwargs = filler.fill(**filler_kwargs)
        return self.function(*(previous_results + new_args), **new_kwargs)

    def name(self):
        return str(self.uuid)

    def function_name(self):
        return self._metadata_function.__name__
