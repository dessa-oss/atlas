"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class StagedModulePy2Loader(object):
    def __init__(self, inner_module):
        from foundations_internal.staged_module_internal_loader import StagedModuleInternalLoader
        self._inner_loader = StagedModuleInternalLoader(inner_module)

    def load_module(self, fullname):
        from imp import new_module
        from sys import modules

        if fullname in modules:
            return modules[fullname]

        new_module = new_module(fullname)
        modules[fullname] = new_module

        self._inner_loader.exec_module(new_module)

        return new_module
