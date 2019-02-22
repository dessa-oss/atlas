"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, patch, call

from foundations_contrib.obfuscator import Obfuscator
from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let, let_mock, set_up, let_patch_mock

class TestObfuscator(Spec):

    mock_subprocess_run = let_patch_mock('subprocess.run')
    mock_os_walk = let_patch_mock('os.walk')

    def test_obfuscate_calls_pyarmor(self):
        obfuscator = Obfuscator()
        obfuscator._obfuscate('/fake/path')
        self.mock_subprocess_run.assert_called_with(['pyarmor', 'obfuscate', '--src=/fake/path'])

    def test_obfuscate_calls_pyarmor_with_entrypoint(self):
        obfuscator = Obfuscator()
        obfuscator._obfuscate('/fake/path', 'fake_script.py')
        self.mock_subprocess_run.assert_called_with(['pyarmor', 'obfuscate', '--src=/fake/path', '--entry=fake_script.py'])

    @patch.object(Obfuscator, '_obfuscate')
    def test_obfuscate_all_calls_obfuscate_recursively(self, mock_obfuscate):
        self.mock_os_walk.return_value = [
            ('/fake_root', ['fake_child_dir_1', 'fake_child_dir_2'], ['fake_file_1']),
            ('/fake_root/fake_child_dir_1', [], []),
        ]
        Obfuscator().obfuscate_all('/fake_root')
        call_1 = call('/fake_root')
        call_2 = call('/fake_root/fake_child_dir_1')
        mock_obfuscate.assert_has_calls([call_1, call_2])
