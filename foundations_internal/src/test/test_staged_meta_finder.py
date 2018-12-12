"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_internal.staged_meta_finder import StagedMetaFinder


class TestStagedMetaFinder(unittest.TestCase):
    class MockModule(object):
        def __init__(self):
            self.__file__ = None

    def test_find_spec_is_a_meta_path_finder(self):
        from importlib.abc import MetaPathFinder

        result = StagedMetaFinder()
        self.assertIsInstance(result, MetaPathFinder)

    def test_find_spec_returns_none_when_module_missing(self):
        result = StagedMetaFinder().find_spec('hello', None, None)
        self.assertEqual(result, None)

    def test_find_spec_returns_spec_when_module_staged(self):
        from importlib._bootstrap import ModuleSpec

        result = StagedMetaFinder().find_spec('staged_pandas', None, None)
        self.assertIsInstance(result, ModuleSpec)

    def test_find_spec_spec_uses_staged_loader(self):
        from foundations_internal.staged_module_loader import StagedModuleLoader

        result = StagedMetaFinder().find_spec('staged_pandas', None, None)
        self.assertIsInstance(result.loader, StagedModuleLoader)

    def test_find_spec_spec_uses_module_name(self):
        result = StagedMetaFinder().find_spec('staged_pandas', None, None)
        self.assertEqual(result.name, 'staged_pandas')

    def test_find_spec_spec_uses_module_name_with_different_name(self):
        result = StagedMetaFinder().find_spec('staged_pickle', None, None)
        self.assertEqual(result.name, 'staged_pickle')

    def test_find_spec_loader_loads_module(self):
        import random

        loader = StagedMetaFinder().find_spec('staged_random', None, None).loader
        module = self.MockModule()
        loader.exec_module(module)
        self.assertEqual(module.__file__, random.__file__)

    def test_find_spec_loader_loads_module_with_different_module(self):
        import pickle

        loader = StagedMetaFinder().find_spec('staged_pickle', None, None).loader
        module = self.MockModule()
        loader.exec_module(module)
        self.assertEqual(module.__file__, pickle.__file__)
