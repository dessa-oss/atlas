"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, patch
from pathlib import Path

from foundations_contrib.cli.scaffold import Scaffold

class TestScaffold(unittest.TestCase):

    def setUp(self):
        self._project_mock = Mock()
    
    @patch('foundations_contrib.cli.project.Project')
    def test_scaffold_project_creates_correct_project(self, project_class_mock):
        scaffold = Scaffold('my project')
        scaffold.scaffold_project()
        project_class_mock.assert_called_with('my project')
    
    @patch('foundations_contrib.cli.project.Project')
    def test_scaffold_project_creates_correct_project_different_project(self, project_class_mock):
        scaffold = Scaffold('my other project')
        scaffold.scaffold_project()
        project_class_mock.assert_called_with('my other project')
    
    @patch('foundations_contrib.root')
    @patch('distutils.dir_util.copy_tree')
    @patch('foundations_contrib.cli.project.Project')
    def test_scaffold_project_copies_directory(self, project_class_mock, copy_mock, root_mock):
        self._project_mock.string_path.return_value = '/path/to/my project'
        self._project_mock.exists.return_value = False
        project_class_mock.return_value = self._project_mock

        root_mock.return_value = Path('/path/to/foundations/root')

        scaffold = Scaffold('my project')
        scaffold.scaffold_project()
        copy_mock.assert_called_with('/path/to/foundations/root/resources/template', '/path/to/my project')
    
    @patch('distutils.dir_util.copy_tree')
    @patch('foundations_contrib.cli.project.Project')
    def test_scaffold_project_returns_true_if_project_does_not_exist(self, project_class_mock, copy_mock):
        self._project_mock.exists.return_value = False
        project_class_mock.return_value = self._project_mock

        scaffold = Scaffold('my project')
        self.assertTrue(scaffold.scaffold_project())
    
    @patch('foundations_contrib.cli.project.Project')
    def test_scaffold_project_returns_false_if_project_exists(self, project_class_mock):
        self._project_mock.exists.return_value = True
        project_class_mock.return_value = self._project_mock

        scaffold = Scaffold('my project')
        self.assertFalse(scaffold.scaffold_project())
    
    @patch('foundations_contrib.root')
    @patch('distutils.dir_util.copy_tree')
    @patch('foundations_contrib.cli.project.Project')
    def test_scaffold_project_copies_directory_different_paths(self, project_class_mock, copy_mock, root_mock):
        self._project_mock.string_path.return_value = '/different/path/to/my other project'
        self._project_mock.exists.return_value = False
        project_class_mock.return_value = self._project_mock

        root_mock.return_value = Path('/path/to/different/foundations/root')

        scaffold = Scaffold('my project')
        scaffold.scaffold_project()
        copy_mock.assert_called_with('/path/to/different/foundations/root/resources/template', '/different/path/to/my other project')
    
    @patch('distutils.dir_util.copy_tree')
    @patch('foundations_contrib.cli.project.Project')
    def test_scaffold_project_copies_directory_project_exists(self, project_class_mock, copy_mock):
        self._project_mock.exists.return_value = True
        project_class_mock.return_value = self._project_mock

        scaffold = Scaffold('my project')
        scaffold.scaffold_project()
        copy_mock.assert_not_called()