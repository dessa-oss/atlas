"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.staged_meta_helper import StagedMetaHelper


class StagedMetaPy2Finder(object):

    def find_module(self, fullname, path=None):
        """Find a module spec for loading

        Arguments:
          fullname {str} -- Name of the module
          path {str} -- Unused

        Returns:
          vcat.StagedModulePy2Loader -- the staged loader for loading the module
        """

        inner_module = StagedMetaHelper(fullname).inner_module()
        if inner_module is not None:
            from vcat.staged_module_py2_loader import StagedModulePy2Loader
            return StagedModulePy2Loader(inner_module)

        return None
