"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, patch, call

from foundations_contrib.obfuscator import Obfuscator
from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import let, let_mock, set_up, let_patch_mock

class TestObfuscator(Spec):

    mock_subprocess_run = let_patch_mock('subprocess.run')
    mock_os_walk = let_patch_mock('os.walk')
    mock_os_chdir = let_patch_mock('os.chdir')
    mock_shutil_rmtree = let_patch_mock('shutil.rmtree')

    def test_obfuscate_calls_pyarmor(self):
        obfuscator = Obfuscator()
        obfuscator.obfuscate('/fake/path')
        self.mock_subprocess_run.assert_called_with(['pyarmor', 'obfuscate', '--src=.'])
    
    def test_obfuscate_calls_os_chdir_with_path_to_obfuscate(self):
        obfuscator = Obfuscator()
        obfuscator.obfuscate('/fake/path')
        self.mock_os_chdir.assert_called_with('/fake/path')

    def test_obfuscate_calls_pyarmor_with_entrypoint(self):
        obfuscator = Obfuscator()
        obfuscator.obfuscate('/fake/path', 'fake_script.py')
        self.mock_subprocess_run.assert_called_with(['pyarmor', 'obfuscate', '--src=.', '--entry=fake_script.py'])

    @patch.object(Obfuscator, 'obfuscate')
    def test_obfuscate_all_calls_obfuscate_recursively(self, mock_obfuscate):
        self.mock_os_walk.return_value = [
            ('/fake_root', ['fake_child_dir_1', 'fake_child_dir_2'], ['fake_file_1']),
            ('/fake_root/fake_child_dir_1', [], []),
        ]
        
        list(Obfuscator().obfuscate_all('/fake_root'))
        call_1 = call('/fake_root')
        call_2 = call('/fake_root/fake_child_dir_1')
        mock_obfuscate.assert_has_calls([call_1, call_2])
    
    @patch.object(Obfuscator, 'obfuscate')
    def test_obfuscate_all_calls_obfuscate_except_on_pycache(self, mock_obfuscate):
        self.mock_os_walk.return_value = [
            ('/fake_root', ['fake_child_dir_1', '__pycache__'], ['fake_file_1']),
            ('/fake_root/__pycache__', [], [])
        ]
        list(Obfuscator().obfuscate_all('/fake_root'))
        mock_obfuscate.assert_called_once_with('/fake_root')

    @patch.object(Obfuscator, 'obfuscate')
    def test_obfuscate_all_yields_root_dir(self, mock_obfuscate):
        self.mock_os_walk.return_value = [
            ('/fake_root', ['fake_child_dir_1', '__pycache__'], ['fake_file_1']),
            ('/fake_root/fake_child_dir_1', [], [])
        ]
        obfuscated_directories_generator = Obfuscator().obfuscate_all('/fake_root')
        self.assertEqual(next(obfuscated_directories_generator), '/fake_root/dist')
        self.assertEqual(next(obfuscated_directories_generator), '/fake_root/fake_child_dir_1/dist')

    def test_cleanup_calls_rmtree_on_one_directory(self):
        self.mock_os_walk.return_value = [
            ('/fake_root', ['fake_child_dir_1', 'dist'], ['fake_file_1']),
            ('/fake_root/dist', [], ['fake_file_2']),
        ]
        Obfuscator().cleanup('/fake_root')
        self.mock_shutil_rmtree.assert_called_once_with('/fake_root/dist')

    def test_cleanup_calls_rmtree_on_multiple_directories(self):
        self.mock_os_walk.return_value = [
            ('/fake_root', ['fake_child_dir_1', 'dist'], ['fake_file_1']),
            ('/fake_root/dist', [], ['fake_file_2']),
            ('/fake_root/fake_child_dir_1', ['dist'], ['fake_file_3']),
            ('/fake_root/fake_child_dir_1/dist', [], ['fake_file_4']),
        ]
        Obfuscator().cleanup('/fake_root')
        call_1 = call('/fake_root/dist')
        call_2 = call('/fake_root/fake_child_dir_1/dist')
        self.mock_shutil_rmtree.assert_has_calls([call_1, call_2])


