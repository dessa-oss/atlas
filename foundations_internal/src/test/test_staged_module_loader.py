"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_internal.staged_module_loader import StagedModuleLoader
from foundations.stage_connector_wrapper import StageConnectorWrapper


class TestStagedModuleLoader(unittest.TestCase):
    class MockModule(object):
        def __init__(self):
            self._pi = None
            self.__file__ = None

            def fake_dumps(obj):
                return lambda: None
            self.dumps = fake_dumps

    def test_loader_is_loader(self):
        from importlib.abc import Loader

        result = StagedModuleLoader(None)
        self.assertIsInstance(result, Loader)

    def test_create_module_returns_none(self):
        result = StagedModuleLoader(None).create_module(None)
        self.assertEqual(None, result)

    def test_exec_module_loads_vars(self):
        import pickle
        module = self.MockModule()
        StagedModuleLoader(pickle).exec_module(module)
        self.assertEqual(pickle.__file__, module.__file__)

    def test_exec_module_loads_vars_from_different_module(self):
        import random
        module = self.MockModule()
        StagedModuleLoader(random).exec_module(module)
        self.assertEqual(random._pi, module._pi)

    def test_exec_module_creates_stages_from_function(self):
        import dill as pickle
        module = self.MockModule()
        StagedModuleLoader(pickle).exec_module(module)
        result = module.dumps('hello')
        self.assertIsInstance(result, StageConnectorWrapper)

    def test_exec_module_stage_function_executes_function(self):
        import dill as pickle
        module = self.MockModule()
        StagedModuleLoader(pickle).exec_module(module)
        result = module.dumps('hello').run_same_process()
        self.assertTrue(pickle.loads(result), 'hello')

    def test_exec_module_stage_function_supports_kwargs(self):
        import dill as pickle
        module = self.MockModule()
        StagedModuleLoader(pickle).exec_module(module)
        result = module.dumps(obj='hello').run_same_process()
        self.assertTrue(pickle.loads(result), 'hello')
