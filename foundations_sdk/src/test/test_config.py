"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 03 2019
"""

from foundations_spec import *


class TestConfig(Spec):

    @let
    def path(self):
        return self.faker.uri_path()

    @let
    def environment_name(self):
        return self.faker.name()

    mock_environment_fetcher = let_patch_instance('foundations_contrib.cli.environment_fetcher.EnvironmentFetcher')
    mock_config_manager = let_patch_mock('foundations_contrib.global_state.config_manager')

    @set_up
    def set_up(self):
        self.mock_environment_fetcher.find_environment = ConditionalReturn()
        self.mock_environment_fetcher.find_environment.return_when(self.path, self.environment_name)
    
    def test_adds_simple_configuration_to_config_manager(self):
        from foundations.config import set_environment        

        set_environment(self.environment_name)
        self.mock_config_manager.add_simple_config_path.assert_called_with(self.path)
