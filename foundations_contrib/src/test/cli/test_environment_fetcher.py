"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock
from foundations_contrib.cli.environment_fetcher import EnvironmentFetcher
from mock import patch
from pathlib import Path

class TestEnvironmentFetcher(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_environment_fetcher_checks_local_config_wrong_directory(self):
        self.assertEqual(EnvironmentFetcher()._get_local_environments(), "Wrong directory")

    @patch('os.listdir', lambda: ['config'])
    def test_environment_fetcher_checks_local_config_empty(self):
        self.assertEqual(EnvironmentFetcher()._get_local_environments(), [])
    
    @patch('os.getcwd', lambda: 'home/some/project')
    @patch('os.listdir')
    @patch('glob.glob')
    def test_environment_fetcher_checks_local_config_one_yaml(self, mock_glob, mock_list):
        mock_glob.return_value = ['home/some/project/config/local.config.yaml']
        mock_list.return_value = ['config']
        self.assertEqual(EnvironmentFetcher()._get_local_environments(), ['home/some/project/config/local.config.yaml'])
    
    @patch('os.getcwd', lambda: 'home/some/project')
    @patch('os.listdir')
    @patch('glob.glob')
    def test_environment_fetcher_checks_local_config_multiple_yaml(self, mock_glob, mock_list):
        yamls = [
            'home/some/project/config/local.config.yaml',
            'home/some/project/config/uat.config.yaml',
            'home/some/project/config/some.config.yaml',
            ]
        mock_glob.return_value = yamls
        mock_list.return_value = ['config']
        self.assertEqual(EnvironmentFetcher()._get_local_environments(), yamls)

    def test_environment_fetcher_checks_global_config_empty(self):
        self.assertEqual(EnvironmentFetcher()._get_global_environments(), [])

    @patch('glob.glob')
    def test_environment_fetcher_checks_global_config_one_yaml(self, mock_glob):
        mock_glob.return_value = ['~/.foundations/config/local.config.yaml']
        self.assertEqual(EnvironmentFetcher()._get_global_environments(), ['~/.foundations/config/local.config.yaml'])
    
    @patch('glob.glob')
    def test_environment_fetcher_checks_global_config_multiple_yaml(self, mock_glob):
        yamls = [
            '~/.foundations/config/local.config.yaml',
            '~/.foundations/config/hippo.config.yaml'
            ]
        mock_glob.return_value = yamls
        self.assertEqual(EnvironmentFetcher()._get_global_environments(), yamls)

    @patch('os.getcwd', lambda: 'home/some/project')
    @patch('os.listdir', lambda: [])
    def test_get_all_environments_returns_error_message_in_wrong_dir(self):
        self.assertEqual(EnvironmentFetcher().get_all_environments(), "Wrong directory")

    
    @patch.object(EnvironmentFetcher, '_get_local_environments')
    @patch.object(EnvironmentFetcher, '_get_global_environments')
    def test_get_all_environments_returns_local_and_global_configs(self, global_mock, local_mock):
        global_mock.return_value = ['123']
        local_mock.return_value = ['456']
        self.assertListEqual(EnvironmentFetcher().get_all_environments(), ['456', '123'])
    

    @patch.object(EnvironmentFetcher, 'get_all_environments')
    def test_find_environment_no_environment(self, env_mock):
        env_mock.return_value = ['/home/hairy.config.yaml']
        env_name = 'local'
        self.assertListEqual(EnvironmentFetcher().find_environment(env_name), [])
    
    @patch.object(EnvironmentFetcher, 'get_all_environments')
    def test_find_environment_one_matching_environment(self, env_mock):
        env_mock.return_value = ['/home/local.config.yaml']
        env_name = 'local'
        self.assertListEqual(EnvironmentFetcher().find_environment(env_name), ['/home/local.config.yaml'])
    
    @patch.object(EnvironmentFetcher, 'get_all_environments')
    def test_find_environment_multiple_matching_environments(self, env_mock):
        env_mock.return_value = ['/home/local.config.yaml', '~/config/local.config.yaml']
        env_name = 'local'
        self.assertListEqual(EnvironmentFetcher().find_environment(env_name), ['/home/local.config.yaml', '~/config/local.config.yaml'])