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
        import os
        def __init__(self):
            self._pi = None
            self.__file__ = __name__
            self.module_directory = 'foundations_sdk/src/test'

    def test_module_directories_and_names_with_name(self):
        import sys
        module_manager = ModuleManager()
        module = module_manager.append_module(sys.modules[__name__])
        for module_name, module_directory in module_manager.module_directories_and_names():
            self.assertEqual('test.test_module_manager', module_name)

    def test_module_directories_and_names_with_name_with_mock_module(self):
        import sys
        module = self.MockModule()
        module_manager = ModuleManager()
        appended_module = module_manager.append_module(sys.modules[__name__])
        for module_name, module_directory in module_manager.module_directories_and_names():
            self.assertEqual(module.__file__, module_name)

    def test_module_directories_and_names_with_directory_with_mock_module(self):
        import sys
        mock_module = self.MockModule()
        module_manager = ModuleManager()
        appended_module = module_manager.append_module(sys.modules[__name__])
        for module_name, module_directory in module_manager.module_directories_and_names():
            self.assertEqual(mock_module.module_directory, (module_directory.split('/foundations/'))[1] )

    def test_module_directories_and_names_with_directory_with_mock_module(self):
        import sys
        mock_module = self.MockModule()
        module_manager = ModuleManager()
        appended_module = module_manager.append_module(sys.modules[__name__])
        for module_name, module_directory in module_manager.module_directories_and_names():
            self.assertEqual(mock_module.module_directory, (module_directory.split('/foundations/'))[1] )