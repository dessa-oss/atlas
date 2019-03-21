"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 03 2019
"""

def set_environment(environment_name):
    from foundations_contrib.cli.environment_fetcher import EnvironmentFetcher
    from foundations_contrib.global_state import config_manager

    environment_fetcher = EnvironmentFetcher()
    path = environment_fetcher.find_environment(environment_name)

    config_manager.add_simple_config_path(path)