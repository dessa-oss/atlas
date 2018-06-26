from importlib.abc import Loader


class StagedModuleLoader(Loader):
    def __init__(self, inner_module):
        self._inner_module = inner_module

    def exec_module(self, module):
        def make_stage(function):
            def stage(*args, **kwargs):
                from vcat import pipeline
                return pipeline.stage(function, *args, **kwargs)
            return stage

        for key, value in vars(self._inner_module).items():
            if callable(value):
                setattr(module, key, make_stage(value))
            else:
                setattr(module, key, value)

  