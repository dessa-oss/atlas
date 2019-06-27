"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Foundations Team <pairing@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_contrib.config_manager import ConfigManager
from foundations.deploy import deploy

class TestDeploy(Spec):

    mock_file = let_mock()
    config_manager = let_patch_mock('foundations.config_manager', ConfigManager())
    mock_open = let_patch_mock('builtins.open')
    mock_yaml_load = let_patch_mock('yaml.load', ConditionalReturn())

    @let_now
    def fake_cwd(self):
        cwd_path = self.faker.file_path()
        patched_os_getcwd = self.patch('os.getcwd')
        patched_os_getcwd.return_value = cwd_path
        return cwd_path

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def environment(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        from foundations_contrib.global_state import current_foundations_context
        self._old_project_name = current_foundations_context().project_name()

        config = {
            'job_deployment_env': 'local',
            'results_config': {},
            'cache_config': {}
        }

        self.mock_yaml_load.return_when(config, self.mock_file)

        self.mock_file.__enter__ = lambda *args: self.mock_file
        self.mock_file.__exit__ = lambda *args: None

        self.mock_open.return_value = self.mock_file

    @tear_down
    def tear_down(self):
        from foundations_contrib.global_state import current_foundations_context
        current_foundations_context().set_project_name(self._old_project_name)

    def test_deploy_with_defaults_sets_project_name_to_cwd_basename(self):
        import os.path as path

        cwd_name = path.basename(self.fake_cwd)
        self._test_deploy_correctly_sets_project_name(cwd_name)

    def test_deploy_with_project_name_specified_sets_project_name_to_project_name(self):
        self._test_deploy_correctly_sets_project_name(self.project_name, project_name=self.project_name)

    def test_deploy_with_defaults_adds_local_config_path_from_global_configs(self):
        deploy()
        self.assertIn('~/.foundations/config/local.config.yaml', self.config_manager.config_paths())

    def test_deploy_with_defaults_adds_path_for_specified_config(self):
        deploy(env=self.environment)
        self.assertIn('~/.foundations/config/{}.config.yaml'.format(self.environment), self.config_manager.config_paths())

    def _test_deploy_correctly_sets_project_name(self, expected_project_name, **kwargs):
        from foundations_contrib.global_state import current_foundations_context

        deploy(**kwargs)
        self.assertEqual(expected_project_name, current_foundations_context().project_name())