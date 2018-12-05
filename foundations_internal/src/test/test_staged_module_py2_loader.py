"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_internal.staged_module_py2_loader import StagedModulePy2Loader
from foundations.stage_connector_wrapper import StageConnectorWrapper


class TestStagedModulePy2Loader(unittest.TestCase):
    def test_load_module_loads_vars(self):
        import pickle

        module = StagedModulePy2Loader(pickle).load_module('staged_pickle')
        self.assertEqual(pickle.__file__, module.__file__)

    def test_load_module_loads_vars_from_different_module(self):
        import random

        module = StagedModulePy2Loader(random).load_module('staged_random')
        self.assertEqual(random._pi, module._pi)

    def test_load_module_creates_stages_from_function(self):
        import dill as pickle

        module = StagedModulePy2Loader(pickle).load_module('staged_dill')
        result = module.dumps('hello')
        self.assertIsInstance(result, StageConnectorWrapper)

    def test_load_module_stage_function_executes_function(self):
        import dill as pickle

        module = StagedModulePy2Loader(pickle).load_module('staged_dill')
        result = module.dumps('hello').run_same_process()
        self.assertTrue(pickle.loads(result), 'hello')

    def test_load_module_stage_function_supports_kwargs(self):
        import dill as pickle

        module = StagedModulePy2Loader(pickle).load_module('staged_dill')
        result = module.dumps(obj='hello').run_same_process()
        self.assertTrue(pickle.loads(result), 'hello')

    def test_load_module_stores_sys_module(self):
        import sys
        import pickle

        module = StagedModulePy2Loader(pickle).load_module('staged_dill')
        self.assertDictContainsSubset({'staged_dill': module}, sys.modules)

    def test_load_module_uses_stored_module(self):
        import sys
        import pickle

        stored_module = StagedModulePy2Loader(
            pickle).load_module('staged_dill')
        module = StagedModulePy2Loader(pickle).load_module('staged_dill')
        self.assertEqual(stored_module, module)
