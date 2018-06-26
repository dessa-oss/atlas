from importlib.abc import Loader


class StagedModuleLoader(Loader):

    def __init__(self, inner_module):
        """Used to create cloned modules with functions replaced with stages

        Arguments:
          inner_module {module} -- Module to duplicate
        """

        self._inner_module = inner_module

    def exec_module(self, module):
        """Copies #inner_module to module and replaces all callables with stages

        Arguments:
          module {module} -- Target module to copy to
        """

        for key, value in self._source_items():
            setattr(module, key, self._callable_to_stage_or_value(value))

    def _callable_to_stage_or_value(self, value):
        if callable(value):
            return StagedModuleLoader._make_stage(value)
        else:
            return value

    def _source_items(self):
        return vars(self._inner_module).items()

    @staticmethod
    def _make_stage(function):
        def stage(*args, **kwargs):
            from vcat import pipeline
            return pipeline.stage(function, *args, **kwargs)
        return stage
