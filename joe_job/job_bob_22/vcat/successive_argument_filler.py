from vcat.argument_filler import ArgumentFiller


class SuccessiveArgumentFiller(object):

    def __init__(self, fill_types, *args, **kwargs):
        self.fills = [fill_type() for fill_type in fill_types]
        self.start_args = args
        self.start_kwargs = kwargs

    def fill(self, **fill_kwargs):
        args = self.start_args
        kwargs = self.start_kwargs
        for fill in self.fills:
            filler = ArgumentFiller(fill, *args, **kwargs)
            args, kwargs = filler.fill(**fill_kwargs)
        return args, kwargs
