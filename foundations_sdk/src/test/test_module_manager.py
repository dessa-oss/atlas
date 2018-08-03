
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
        def __init__(self, file, name):
            self.__file__ = file
            self.__name__ = name

    def test_module_directories_and_names_returns_name_and_directory(self):
        module_manager = ModuleManager()
        mock_module = self.MockModule(
            '/path/to/some/python/file.py', 'python.file')

        module_manager.append_module(mock_module)
        result_module_directories = list(
            module_manager.module_directories_and_names())
        expected_module_directories = [('python.file', '/path/to/some/python')]
        self.assertEqual(expected_module_directories,
                         result_module_directories)

    def test_module_directories_and_names_with_different_name_and_path(self):
        module_manager = ModuleManager()
        mock_module = self.MockModule(
            '/another/file/path/file.py', 'another.pythonfile')

        module_manager.append_module(mock_module)
        result_module_directories = list(
            module_manager.module_directories_and_names())
        expected_module_directories = [
            ('another.pythonfile', '/another/file/path')]
        self.assertEqual(expected_module_directories,
                         result_module_directories)

    def test_module_directories_and_names_with_mutliple_names_and_directories(self):
        module_manager = ModuleManager()
        mock_module = self.MockModule(
            '/path/to/some/python/file.py', 'python.file')
        mock_module_two = self.MockModule(
            '/another/file/path/file.py', 'another.pythonfile')

        module_manager.append_module(mock_module)
        module_manager.append_module(mock_module_two)

        result_module_directories = list(
            module_manager.module_directories_and_names())
        expected_module_directories = [
            ('python.file', '/path/to/some/python'), ('another.pythonfile', '/another/file/path')]
        self.assertEqual(expected_module_directories,
                         result_module_directories)

    def test_module_directories_return_absolute_path(self):
        from os import getcwd

        module_manager = ModuleManager()
        mock_module = self.MockModule(
            'python/file.py', 'python.file')
        module_manager.append_module(mock_module)
        
        result_module_directories = list(
            module_manager.module_directories_and_names())
        expected_module_directories = [('python.file', '{}/python'.format(getcwd()))]

        self.assertEquals(expected_module_directories, result_module_directories)
    

    def test_module_directories_return_absolute_path_even_if_cwd_changes(self):
        from os import getcwd
        from foundations import ChangeDirectory

        module_manager = ModuleManager()
        mock_module = self.MockModule(
            'python/file.py', 'python.file')
        module_manager.append_module(mock_module)
        
        expected_module_directories = [('python.file', '{}/python'.format(getcwd()))]
        with ChangeDirectory('/etc'):
            result_module_directories = list(
                module_manager.module_directories_and_names())
            self.assertEquals(expected_module_directories, result_module_directories)