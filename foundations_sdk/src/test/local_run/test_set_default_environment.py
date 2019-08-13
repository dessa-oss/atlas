"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations.local_run import load_local_configuration_if_present

class SetDefaultEnvironment(Spec):

    mock_environment_fetcher = let_patch_instance('foundations_contrib.cli.environment_fetcher.EnvironmentFetcher')
    mock_set_environment = let_patch_mock('foundations.config.set_environment')

    def test_default_environment_loaded_when_present_locally(self):
        self.mock_environment_fetcher.get_all_environments.return_value = (['default'], [])
        load_local_configuration_if_present()
        self.mock_set_environment.assert_called_with('default')

    def test_default_environment_loaded_when_present_globally(self):
        self.mock_environment_fetcher.get_all_environments.return_value = ([], ['default'])
        load_local_configuration_if_present()
        self.mock_set_environment.assert_called_with('default')

    def test_default_environment_not_loaded_when_absent(self):
        self.mock_environment_fetcher.get_all_environments.return_value = ([], [])
        load_local_configuration_if_present()
        self.mock_set_environment.assert_not_called()
    
    def test_default_environment_not_loaded_when_no_environments(self):
        self.mock_environment_fetcher.get_all_environments.return_value = (None, None)
        load_local_configuration_if_present()
        self.mock_set_environment.assert_not_called()

    