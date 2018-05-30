class Stage(object):

    def __init__(self, uuid, function, metadata_function, *args, **kwargs):
        self._uuid = uuid
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self._metadata_function = metadata_function

    def uuid(self):
        return self._uuid

    def run(self, previous_results, filler_builder, **filler_kwargs):
        new_args, new_kwargs = self.fill_args_and_kwargs(filler_builder, **filler_kwargs)
        return self.function(*(previous_results + new_args), **new_kwargs)

    def filler(self, filler_builder):
        return filler_builder(*self.args, **self.kwargs)

    def fill_args_and_kwargs(self, filler_builder, **filler_kwargs):
        return self.filler(filler_builder).fill(**filler_kwargs)

    def name(self):
        return str(self.uuid())

    def function_name(self):
        return self._metadata_function.__name__
    
    def function_source_code(self):
        import inspect
        return inspect.getsource(self._metadata_function)
    
    def source_file(self):
        import inspect
        return inspect.getsourcefile(self._metadata_function)

    def source_line(self):
        import inspect
        return inspect.getsourcelines(self._metadata_function)[1]