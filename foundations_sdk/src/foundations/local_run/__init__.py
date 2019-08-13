"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def load_local_configuration_if_present():
    from foundations.config import set_environment
    from foundations_contrib.cli.environment_fetcher import EnvironmentFetcher
    
    environment_fetcher = EnvironmentFetcher()

    local_environments, global_environments = environment_fetcher.get_all_environments()
    if local_environments and 'default' in local_environments or global_environments and 'default' in global_environments:
        set_environment('default')
