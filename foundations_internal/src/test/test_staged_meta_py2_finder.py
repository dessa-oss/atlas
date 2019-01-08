"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_internal.staged_meta_py2_finder import StagedMetaPy2Finder


class TestStagedMetaPy2Finder(unittest.TestCase):
    def test_find_module_returns_none_when_module_missing(self):
        result = StagedMetaPy2Finder().find_module('hello', None)
        self.assertEqual(result, None)

    def test_find_module_spec_uses_staged_loader(self):
        from foundations_internal.staged_module_py2_loader import StagedModulePy2Loader

        result = StagedMetaPy2Finder().find_module('staged_pandas', None)
        self.assertIsInstance(result, StagedModulePy2Loader)

    def test_find_module_loader_loads_module(self):
        import random

        loader = StagedMetaPy2Finder().find_module('staged_random', None)
        module = loader.load_module('staged_random')
        self.assertEqual(module.__file__, random.__file__)

    def test_find_module_loader_loads_module_with_different_module(self):
        import pickle

        loader = StagedMetaPy2Finder().find_module('staged_pickle', None)
        module = loader.load_module('staged_pickle')
        self.assertEqual(module.__file__, pickle.__file__)
