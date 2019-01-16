"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from unittest.mock import patch, call
from pathlib import Path
from distutils.dir_util import copy_tree

from scaffold import Scaffold


class TestScaffold(unittest.TestCase):

    def test_get_project_name(self):
        mock_args = ['blah', 'init', 'my-foundations-project']
        expected_args = "my-foundations-project"
        scaffold = Scaffold()

        with patch('sys.argv', mock_args):
            self.assertEqual(scaffold.get_project_name(), expected_args)

    def test_get_command(self):
        mock_args = ['blah', 'init']
        expected_args = "init"
        scaffold = Scaffold()

        with patch('sys.argv', mock_args):
            scaffold.get_command()
            self.assertEqual(scaffold.command, expected_args)
