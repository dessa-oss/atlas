"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, patch

from foundations_contrib.obfuscator import Obfuscator
from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let, let_mock, set_up, let_patch_mock

class TestObfuscator(Spec):

    mock_subprocess_run = let_patch_mock('subprocess.run')
    
    def test_obfuscate_calls_pyarmor(self):
        self.mock_subprocess_run
        obfuscator = Obfuscator()
        obfuscator.obfuscate('/fake/path')
        self.mock_subprocess_run.assert_called_with(['pyarmor', 'obfuscate', '--src=/fake/path'])

    def test_obfuscate_calls_pyarmor_with_entrypoint(self):
        self.mock_subprocess_run
        obfuscator = Obfuscator()
        obfuscator.obfuscate('/fake/path', 'fake_script.py')
        self.mock_subprocess_run.assert_called_with(['pyarmor', 'obfuscate', '--src=/fake/path', '--entry=fake_script.py'])
