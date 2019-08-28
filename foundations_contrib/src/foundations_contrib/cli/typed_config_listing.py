"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class TypedConfigListing(object):
    
    def __init__(self, config_type):
        from foundations_contrib.cli.config_listing import ConfigListing
        from foundations_contrib.utils import foundations_home
        import os.path

        self._config_type = config_type
        self._local_listing = ConfigListing(f'config/{self._config_type}')
        self._foundations_listing = ConfigListing(f'{os.path.expanduser(foundations_home())}/config/{self._config_type}')

    def config_path(self, name):
        return self._local_listing.config_path(name) or self._foundations_listing.config_path(name)

    def config_data(self, name):
        result = self._local_listing.config_data(name) or self._foundations_listing.config_data(name)
        if result is None:
            raise ValueError(f'No {self._config_type} config {name} found')
        return result

