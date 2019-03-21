"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 03 2019
"""

def set_environment(environment_name):
    from foundations_contrib.global_state import config_manager

    path = _environment_path(environment_name)
    config_manager.add_simple_config_path(path)

def _environment_path(environment_name):
    from foundations_contrib.cli.environment_fetcher import EnvironmentFetcher

    environment_fetcher = EnvironmentFetcher()
    paths = environment_fetcher.find_environment(environment_name)
    if paths:
        return paths[0]
    else:
        raise ValueError(_missing_environment_message(environment_name))

def _missing_environment_message(environment_name):
    return 'No environment {} found, please set a valid deployment environment with foundations.set_environment'.format(environment_name)
