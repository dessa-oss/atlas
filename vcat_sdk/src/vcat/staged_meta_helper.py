"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class StagedMetaHelper(object):
    """Used to create define specs for loading staged modules in importing modules
    """

    STAGED_PREFIX = 'staged_'
    STAGED_PREFIX_LENGTH = len(STAGED_PREFIX)

    def __init__(self, fullname):
        self._fullname = fullname

    def inner_module(self):
        if self._is_staged_module():
            return self._find_module()

    def _find_module(self):
        from importlib import import_module

        module_name = self._module_without_staged_prefix()
        return import_module(module_name)

    def _module_without_staged_prefix(self):
        return self._fullname[StagedMetaHelper.STAGED_PREFIX_LENGTH:]

    def _is_staged_module(self):
        return self._fullname.startswith(StagedMetaHelper.STAGED_PREFIX)
