"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, call, patch

import foundations_internal
from foundations_contrib.module_obfuscation_controller import ModuleObfuscationController
from foundations_contrib.obfuscator import Obfuscator
from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let, let_mock, set_up, let_patch_mock


class TestModuleObfuscationController(Spec):

    @staticmethod
    def _return_generator(input):
        for item in input:
            yield item
    
    @let
    def default_config(self):
        from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment
        return {
            'deployment_implementation': {
                'deployment_type': LocalShellJobDeployment
            }
        }

    @patch.object(foundations_internal.module_manager.ModuleManager, 'module_directories_and_names')
    def test_get_foundations_modules_yields_one_module_only(self, mock_module_directories_and_names):

        mock_module_directories_and_names.return_value = TestModuleObfuscationController._return_generator([
            ('fake_module_name', 'fake_module_directory')])
        module_obfuscation_controller = ModuleObfuscationController(self.default_config)
        foundations_modules_generator = module_obfuscation_controller.get_foundations_modules()
        module_name, module_directory =  next(foundations_modules_generator)
        self.assertEqual(module_name, 'fake_module_name')
        self.assertEqual(module_directory, 'fake_module_directory')
        with self.assertRaises(StopIteration):
            next(foundations_modules_generator)
    
    @patch.object(foundations_internal.module_manager.ModuleManager, 'module_directories_and_names')
    def test_get_foundations_modules_yields_two_modules_only(self, mock_module_directories_and_names):
        mock_module_directories_and_names.return_value = TestModuleObfuscationController._return_generator([
            ('fake_module_name', 'fake_module_directory'), ('fake_module_name_2', 'fake_module_directory_2')])
        module_obfuscation_controller = ModuleObfuscationController(self.default_config)
        foundations_modules_generator = module_obfuscation_controller.get_foundations_modules()
        self.assertEqual(next(foundations_modules_generator), ('fake_module_name', 'fake_module_directory'))
        self.assertEqual(next(foundations_modules_generator), ('fake_module_name_2', 'fake_module_directory_2'))
        with self.assertRaises(StopIteration):
            next(foundations_modules_generator)

    def test_is_remote_deployment_returns_true_when_local(self):
        from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment
        module_obfuscation_controller = ModuleObfuscationController(self.default_config)
        self.assertFalse(module_obfuscation_controller._is_remote_deployment())

    def test_is_remote_deployment_returns_false_when_not_local(self):
        from foundations_ssh.sftp_job_deployment import SFTPJobDeployment

        for deployment in SFTPJobDeployment, 'FakeGCPJobDeployment':
            config = {
                'deployment_implementation': {
                    'deployment_type': deployment
                }
            }
            module_obfuscation_controller = ModuleObfuscationController(config)
            self.assertTrue(module_obfuscation_controller._is_remote_deployment())

    def test_need_obfuscation_returns_true_when_in_config(self):
        config = self.default_config
        config['obfuscate'] = True
        module_obfuscation_controller = ModuleObfuscationController(config)
        self.assertTrue(module_obfuscation_controller._need_obfuscation())
    
    def test_need_obfuscation_returns_false_when_not_in_config(self):
        module_obfuscation_controller = ModuleObfuscationController({})
        self.assertFalse(module_obfuscation_controller._need_obfuscation())
    
    def test_need_obfuscation_returns_false_when_in_config(self):
        config = self.default_config
        config['obfuscate'] = False
        module_obfuscation_controller = ModuleObfuscationController(config)
        self.assertFalse(module_obfuscation_controller._need_obfuscation())

    @patch.object(foundations_internal.module_manager.ModuleManager, 'module_directories_and_names')
    @patch.object(Obfuscator, 'obfuscate_all')
    def test_get_foundations_modules_calls_obfuscator_if_obfuscation_needed(self, mock_obfuscator, mock_module_manager):
        from foundations_ssh.sftp_job_deployment import SFTPJobDeployment
        mock_module_manager.return_value = TestModuleObfuscationController._return_generator([('who_cares','obfuscated/return/path')])

        config = {
            'obfuscate': True,
            'deployment_implementation': {
                'deployment_type': SFTPJobDeployment
            }
        }
        module_obfuscation_controller = ModuleObfuscationController(config)
        list(module_obfuscation_controller.get_foundations_modules())
        mock_obfuscator.assert_called_once_with('obfuscated/return/path')

    
    @patch.object(foundations_internal.module_manager.ModuleManager, 'module_directories_and_names')
    @patch.object(Obfuscator, 'obfuscate_all')
    def test_get_foundations_modules_returns_generator_with_correct_abs_path_if_obfuscation_needed(self, mock_obfuscator, mock_module_manager):
        from foundations_ssh.sftp_job_deployment import SFTPJobDeployment
        mock_module_manager.return_value = TestModuleObfuscationController._return_generator([('who_cares','obfuscated/return/path')])
        mock_obfuscator.return_value = TestModuleObfuscationController._return_generator(['obfuscated/return/path/dist'])

        config = {
            'obfuscate': True,
            'deployment_implementation': {
                'deployment_type': SFTPJobDeployment
            }
        }
        module_obfuscation_controller = ModuleObfuscationController(config)

        foundations_modules_generator = module_obfuscation_controller.get_foundations_modules()
        self.assertEqual(next(foundations_modules_generator)[1], 'obfuscated/return/path/dist')
        with self.assertRaises(StopIteration):
            next(foundations_modules_generator)


    @patch.object(foundations_internal.module_manager.ModuleManager, 'module_directories_and_names')
    @patch.object(Obfuscator, 'obfuscate_all')
    def test_get_foundations_modules_returns_generator_with_correct_relative_path_if_obfuscation_needed(self, mock_obfuscator, mock_module_manager):
        from foundations_ssh.sftp_job_deployment import SFTPJobDeployment
        mock_module_manager.return_value = TestModuleObfuscationController._return_generator([('fake_foundations_package', '/abs/path/fake_foundations_package')])
        mock_obfuscator.return_value = TestModuleObfuscationController._return_generator(['/abs/path/fake_foundations_package/dist', '/abs/path/fake_foundations_package/child_package/dist'])

        config = {
            'obfuscate': True,
            'deployment_implementation': {
                'deployment_type': SFTPJobDeployment
            }
        }
        module_obfuscation_controller = ModuleObfuscationController(config)
        foundations_modules_generator = module_obfuscation_controller.get_foundations_modules()
        self.assertEqual(next(foundations_modules_generator)[0], 'fake_foundations_package')
        self.assertEqual(next(foundations_modules_generator)[0], 'fake_foundations_package/child_package')
        with self.assertRaises(StopIteration):
            next(foundations_modules_generator)
            