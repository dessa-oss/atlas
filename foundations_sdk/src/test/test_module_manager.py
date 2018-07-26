"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations.module_manager import ModuleManager


class TestModuleManager(unittest.TestCase):
    class MockModule(object):
        def __init__(self):
            self._pi = None
            self.__file__ = None

            def fake_dumps(obj):
                return lambda: None
            self.dumps = fake_dumps

    def test_module_directories_and_names_with_name(self):
        import sys
        module_manager = ModuleManager()
        module = module_manager.append_module(sys.modules[__name__])
        for module_name, module_directory in module_manager.module_directories_and_names():
            self.assertEqual('test.test_module_manager', module_name)
