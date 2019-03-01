"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import unittest
from mock import Mock, call, patch

from foundations_contrib.job_bundler import JobBundler
from foundations_contrib.obfuscator import Obfuscator
from foundations_contrib.resources_obfuscation_controller import ResourcesObfuscationController
from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let, let_mock, set_up, let_patch_mock

@patch.object(Obfuscator, 'obfuscate')
class TestResourcesObfuscationController(Spec):

    mock_os_dirname = let_patch_mock('os.path.dirname')
    mock_shutil_copyfile = let_patch_mock('shutil.copyfile')

    @let
    def default_config(self):
        from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment
        return {
            'obfuscate_foundations': False,
            'deployment_implementation': {
                'deployment_type': LocalShellJobDeployment
            }
        }
    
    def test_get_resources_returns_resources_directory_if_not_obfuscated(self, mock_obfuscate_fn):
        self.mock_os_dirname.return_value = '/directory/path'
        config = self.default_config
        resources_obfuscation_controller = ResourcesObfuscationController(config)
        self.assertEqual(resources_obfuscation_controller.get_resources(), '/directory/path/resources')

    def test_get_resources_returns_resources_directory_if_not_obfuscated_different_directory(self, mock_obfuscate_fn):
        self.mock_os_dirname.return_value = '/directory/path/different'
        config = self.default_config
        resources_obfuscation_controller = ResourcesObfuscationController(config)
        self.assertEqual(resources_obfuscation_controller.get_resources(), '/directory/path/different/resources')

    def test_get_resources_calls_obfuscate_with_correct_args_if_obfuscated(self, mock_obfuscate_fn):
        self.mock_os_dirname.return_value = '/directory/path'
        config = self.default_config
        config['obfuscate_foundations'] = True
        config['deployment_implementation']['deployment_type'] = 'notLocal'
        resources_obfuscation_controller = ResourcesObfuscationController(config)
        resources_obfuscation_controller.get_resources()
        mock_obfuscate_fn.assert_called_with('/directory/path/resources', script='main.py')

    def test_get_resources_calls_obfuscate_with_correct_args_if_obfuscated_with_different_name(self, mock_obfuscate_fn):
        self.mock_os_dirname.return_value = '/directory/path/different'
        config = self.default_config
        config['obfuscate_foundations'] = True
        config['deployment_implementation']['deployment_type'] = 'notLocal'
        resources_obfuscation_controller = ResourcesObfuscationController(config)
        resources_obfuscation_controller.get_resources()
        mock_obfuscate_fn.assert_called_with('/directory/path/different/resources', script='main.py')

    def test_get_resources_obfuscate_not_called_with_default_config(self, mock_obfuscate_fn):
        self.mock_os_dirname.return_value = '/directory/path'
        config = self.default_config
        resources_obfuscation_controller = ResourcesObfuscationController(config)
        resources_obfuscation_controller.get_resources()
        mock_obfuscate_fn.assert_not_called()

    def test_get_resources_returns_dist_resources_directory_if_obfuscated(self, mock_obfuscate_fn):
        self.mock_os_dirname.return_value = '/directory/path'
        config = self.default_config
        config['obfuscate_foundations'] = True
        config['deployment_implementation']['deployment_type'] = 'notLocal'
        resources_obfuscation_controller = ResourcesObfuscationController(config)
        self.assertEqual(resources_obfuscation_controller.get_resources(), '/directory/path/resources/dist')
    
    def test_get_resources_adds_files_to_dist_resources_directory_if_obfuscated(self, mock_obfuscate_fn):
        self.mock_os_dirname.return_value = '/directory/path'
        config = self.default_config
        config['obfuscate_foundations'] = True
        config['deployment_implementation']['deployment_type'] = 'notLocal'
        resources_obfuscation_controller = ResourcesObfuscationController(config)
        resources_obfuscation_controller.get_resources()
        run_sh_call = call('/directory/path/resources/run.sh', '/directory/path/resources/dist/run.sh')
        foundations_requirements_call = call(
            '/directory/path/resources/foundations_requirements.txt',
            '/directory/path/resources/dist/foundations_requirements.txt')
        self.mock_shutil_copyfile.assert_has_calls([run_sh_call, foundations_requirements_call])

    