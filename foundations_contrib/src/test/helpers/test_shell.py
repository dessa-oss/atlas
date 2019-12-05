"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, patch

import foundations_contrib.helpers.shell as shell

from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import let

class TestShell(Spec):
    
    @let
    def winreg(self):
        # hack to deal with testing on non-windows machines
        module_callback = self.patch('foundations_contrib.helpers.shell._winreg_module')
        module_callback.return_value = Mock()
        return module_callback.return_value

    def test_find_bash_returns_default_bash(self):
        self.assertEqual('/bin/bash', shell.find_bash())

    @patch('os.name', 'nt')
    def test_queries_correct_registry_on_windows(self):
        self.winreg.HKEY_CLASSES_ROOT = 'HKEY_CLASSES_ROOT'
        self.winreg.QueryValue.return_value = 'null 0 0'
        shell.find_bash()
        self.winreg.QueryValue.assert_called_with('HKEY_CLASSES_ROOT', 'Directory\shell\git_shell\command')

    @patch('os.name', 'nt')
    def test_find_bash_returns_bash_on_windows(self):
        self.winreg.QueryValue.return_value = '"C:\\path to\\git-bash.exe" 0 0'
        self.assertEqual('C:\\path to\\bin\\bash.exe', shell.find_bash())

    @patch('os.name', 'nt')
    def test_find_bash_returns_bash_on_windows_different_path(self):
        self.winreg.QueryValue.return_value = '"C:\\Program Files\\git\\git-bash.exe" 3 2'
        self.assertEqual('C:\\Program Files\\git\\bin\\bash.exe', shell.find_bash())


