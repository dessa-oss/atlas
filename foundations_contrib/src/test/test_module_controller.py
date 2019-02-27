"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, call, patch

import foundations_internal
from foundations_contrib.module_controller import ModuleController
from foundations_contrib.obfuscator import Obfuscator
from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let, let_mock, set_up, let_patch_mock


class TestModuleController(Spec):

    @staticmethod
    def _return_generator(input):
        for item in input:
            yield item

    @patch.object(foundations_internal.module_manager.ModuleManager, 'module_directories_and_names')
    def test_get_foundations_modules_yields_one_module_only(self, mock_module_directories_and_names):

        mock_module_directories_and_names.return_value = TestModuleController._return_generator([
            ('fake_module_name', 'fake_module_directory')])
        module_controller = ModuleController({})
        module_name, module_directory =  next(module_controller.get_foundations_modules())
        self.assertEqual(module_name, 'fake_module_name')
        self.assertEqual(module_directory, 'fake_module_directory')
        with self.assertRaises(StopIteration):
            next(module_controller.get_foundations_modules())
    
    @patch.object(foundations_internal.module_manager.ModuleManager, 'module_directories_and_names')
    def test_get_foundations_modules_yields_two_modules_only(self, mock_module_directories_and_names):
        mock_module_directories_and_names.return_value = TestModuleController._return_generator([
            ('fake_module_name', 'fake_module_directory'), ('fake_module_name_2', 'fake_module_directory_2')])
        module_controller = ModuleController({})
        self.assertEqual(next(module_controller.get_foundations_modules()), ('fake_module_name', 'fake_module_directory'))
        self.assertEqual(next(module_controller.get_foundations_modules()), ('fake_module_name_2', 'fake_module_directory_2'))
        with self.assertRaises(StopIteration):
            next(module_controller.get_foundations_modules())


    def test_is_remote_deployment_returns_true_when_local(self):
        from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment

        config = {
            'deployment_implementation': {
                'deployment_type': LocalShellJobDeployment
            }
        }
        module_controller = ModuleController(config)
        self.assertTrue(module_controller._is_remote_deployment())

    def test_is_remote_deployment_returns_false_when_not_local(self):
        from foundations_ssh.sftp_job_deployment import SFTPJobDeployment

        for deployment in SFTPJobDeployment, 'FakeGCPJobDeployment':
            config = {
                'deployment_implementation': {
                    'deployment_type': deployment
                }
            }
            module_controller = ModuleController(config)
            self.assertFalse(module_controller._is_remote_deployment())

    def test_need_obfuscation_returns_true_when_in_config(self):
        config = {'obfuscate': True}
        module_controller = ModuleController(config)
        self.assertTrue(module_controller._need_obfuscation())
    
    def test_need_obfuscation_returns_false_when_not_in_config(self):
        module_controller = ModuleController({})
        self.assertFalse(module_controller._need_obfuscation())
    
    def test_need_obfuscation_returns_false_when_in_config(self):
        config = {'obfuscate': False}
        module_controller = ModuleController(config)
        self.assertFalse(module_controller._need_obfuscation())


