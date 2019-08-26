"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from mock import patch

from foundations_contrib.cli.environment_fetcher import EnvironmentFetcher
from pathlib import Path

class TestEnvironmentFetcher(Spec):

    mock_glob = let_patch_mock('glob.glob')
    mock_list = let_patch_mock('os.listdir')
    
    def test_environment_fetcher_checks_local_config_wrong_directory(self):
        self.assertEqual(EnvironmentFetcher()._get_local_environments(), None)

    @patch('os.listdir', lambda: ['config'])
    def test_environment_fetcher_checks_local_config_empty(self):
        self.mock_glob.return_value = []
        self.assertEqual(EnvironmentFetcher()._get_local_environments(), [])
    
    @patch('os.getcwd', lambda: 'home/some/project')
    def test_environment_fetcher_checks_local_config_one_yaml(self):
        self.mock_glob.return_value = ['home/some/project/config/local.config.yaml']
        self.mock_list.return_value = ['config']
        self.assertEqual(EnvironmentFetcher()._get_local_environments(), ['home/some/project/config/local.config.yaml'])
        self.mock_glob.assert_called_with('home/some/project/config/*.config.yaml')

    @patch('os.getcwd', lambda: 'home/some/project')
    def test_environment_fetcher_checks_local_config_multiple_yaml(self):
        yamls = [
            'home/some/project/config/local.config.yaml',
            'home/some/project/config/uat.config.yaml',
            'home/some/project/config/some.config.yaml',
            ]
        self.mock_glob.return_value = yamls
        self.mock_list.return_value = ['config']
        self.assertEqual(EnvironmentFetcher()._get_local_environments(), yamls)

    def test_environment_fetcher_checks_global_config_empty(self):
        self.mock_glob.return_value = []
        self.assertEqual(EnvironmentFetcher()._get_global_environments(), [])

    def test_environment_fetcher_checks_global_config_one_yaml(self):
        self.mock_glob.return_value = ['~/.foundations/config/local.config.yaml']
        self.assertEqual(EnvironmentFetcher()._get_global_environments(), ['~/.foundations/config/local.config.yaml'])
    
    @patch('os.path.expanduser')
    def test_environment_fetcher_checks_global_config_multiple_yaml(self, mock_user):
        yamls = [
            '~/.foundations/config/local.config.yaml',
            '~/.foundations/config/hippo.config.yaml'
            ]
        self.mock_glob.return_value = yamls
        mock_user.return_value = '/home/.foundations/config'
        self.assertEqual(EnvironmentFetcher()._get_global_environments(), yamls)
        self.mock_glob.assert_called_with('/home/.foundations/config/*.config.yaml')

    
    @patch.object(EnvironmentFetcher, '_get_local_environments')
    @patch.object(EnvironmentFetcher, '_get_global_environments')
    def test_get_all_environments_returns_local_and_global_configs(self, global_mock, local_mock):
        global_mock.return_value = ['123']
        local_mock.return_value = ['456']
        self.assertEqual(EnvironmentFetcher().get_all_environments(), (['456'], ['123']))
    
    @patch.object(EnvironmentFetcher, '_get_local_environments')
    @patch.object(EnvironmentFetcher, '_get_global_environments')
    def test_get_all_environments_returns_local_and_global_configs_wrong_directory(self, global_mock, local_mock):
        global_mock.return_value = ['123']
        local_mock.return_value = None
        self.assertEqual(EnvironmentFetcher().get_all_environments(), (None, ['123']))
    
    @patch.object(EnvironmentFetcher, '_get_local_environments')
    @patch.object(EnvironmentFetcher, '_get_global_environments')
    def test_get_all_environments_returns_local_and_global_configs_no_local(self, global_mock, local_mock):
        global_mock.return_value = ['123']
        local_mock.return_value = []
        self.assertEqual(EnvironmentFetcher().get_all_environments(), ([], ['123']))
    

    @patch.object(EnvironmentFetcher, '_get_local_environments')
    @patch.object(EnvironmentFetcher, '_get_global_environments')
    def test_find_environment_no_environment(self, global_mock, local_mock):
        local_mock.return_value = ['/home/hairy.config.yaml']
        global_mock.return_value = []
        env_name = 'local'
        self.assertListEqual(EnvironmentFetcher().find_environment(env_name), [])
    
    @patch.object(EnvironmentFetcher, '_get_local_environments')
    def test_find_environment_returns_error_message_in_wrong_dir(self, local_mock):
        env_name = 'hi'
        local_mock.return_value = None
        self.assertEqual(EnvironmentFetcher().find_environment(env_name), [])
    
    @patch.object(EnvironmentFetcher, '_get_local_environments')
    @patch.object(EnvironmentFetcher, '_get_global_environments')
    def test_find_environment_one_matching_environment(self, global_mock, local_mock):
        local_mock.return_value = ['/home/local.config.yaml']
        global_mock.return_value = ['/bob.config.yaml']
        env_name = 'local'
        self.assertListEqual(EnvironmentFetcher().find_environment(env_name), ['/home/local.config.yaml'])
    
    @patch.object(EnvironmentFetcher, '_get_local_environments')
    @patch.object(EnvironmentFetcher, '_get_global_environments')
    def test_find_environment_multiple_matching_environments(self, global_mock, local_mock):
        local_mock.return_value = ['/home/local.config.yaml']
        global_mock.return_value = ['/local.config.yaml']
        env_name = 'local'
        self.assertListEqual(EnvironmentFetcher().find_environment(env_name), ['/home/local.config.yaml', '/local.config.yaml'])

    @patch.object(EnvironmentFetcher, '_get_local_environments')
    @patch.object(EnvironmentFetcher, '_get_global_environments')
    def test_find_environment_multiple_matching_environments_returns_correct_basename(self, global_mock, local_mock):
        local_mock.return_value = ['/home/stageless_local.config.yaml']
        global_mock.return_value = ['/local.config.yaml']
        env_name = 'local'
        self.assertListEqual(EnvironmentFetcher().find_environment(env_name), ['/local.config.yaml'])
