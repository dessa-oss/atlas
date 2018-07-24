"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class StagedModuleInternalLoader(object):
    """Used to create cloned modules with functions replaced with stages (internal implementation)

    Arguments:
        inner_module {module} -- Module to duplicate
    """

    def __init__(self, inner_module):
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
            return StagedModuleInternalLoader._make_stage(value)
        else:
            return value

    def _source_items(self):
        return vars(self._inner_module).items()

    @staticmethod
    def _make_stage(function):
        def stage(*args, **kwargs):
            from foundations import pipeline
            return pipeline.stage(function, *args, **kwargs)
        return stage
