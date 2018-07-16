"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from importlib.abc import MetaPathFinder
from foundations.staged_meta_helper import StagedMetaHelper


class StagedMetaFinder(MetaPathFinder):
    """Used to create define specs for loading staged modules in importing modules
    """

    def find_spec(self, fullname, path, target=None):
        """Find a module spec for loading

        Arguments:
          fullname {str} -- Name of the module
          path {str} -- Unused

        Keyword Arguments:
          target {str} -- Unused (default: {None})

        Returns:
          importlib._bootstrap.ModuleSpec -- ModuleSpec containing information required to import the module
        """

        inner_module = StagedMetaHelper(fullname).inner_module()
        if inner_module is not None:
            return self._load_spec(fullname, inner_module)

        return None

    def _load_spec(self, fullname, inner_module):
        from importlib.util import spec_from_file_location
        from foundations.staged_module_loader import StagedModuleLoader

        return spec_from_file_location(fullname, loader=StagedModuleLoader(inner_module))
