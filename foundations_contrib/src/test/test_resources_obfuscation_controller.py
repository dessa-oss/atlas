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

class TestResourcesObfuscationController(Spec):

    mock_os_dirname = let_patch_mock('os.path.dirname')


    @let
    def default_config(self):
        from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment
        return {
            'obfuscate_foundations': False,
            'deployment_implementation': {
                'deployment_type': LocalShellJobDeployment
            }
        }
    

    def test_get_resources_returns_resources_directory_if_not_obfuscated(self):
        self.mock_os_dirname.return_value = '/directory/path'
        config = self.default_config
        resources_obfuscation_controller = ResourcesObfuscationController(config)
        self.assertEqual(resources_obfuscation_controller.get_resources(), '/directory/path/resources')
    
    def test_get_resources_returns_resources_directory_if_not_obfuscated_different_directory(self):
        self.mock_os_dirname.return_value = '/directory/path/different'
        config = self.default_config
        resources_obfuscation_controller = ResourcesObfuscationController(config)
        self.assertEqual(resources_obfuscation_controller.get_resources(), '/directory/path/different/resources')

