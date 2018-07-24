"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from importlib.abc import Loader


class StagedModuleLoader(Loader):
    """Used to create cloned modules with functions replaced with stages

    Arguments:
        inner_module {module} -- Module to duplicate
    """

    def __init__(self, inner_module):
        from foundations.staged_module_internal_loader import StagedModuleInternalLoader
        self._inner_loader = StagedModuleInternalLoader(inner_module)

    def exec_module(self, module):
        """Copies #inner_module to module and replaces all callables with stages

        Arguments:
          module {module} -- Target module to copy to
        """

        self._inner_loader.exec_module(module)