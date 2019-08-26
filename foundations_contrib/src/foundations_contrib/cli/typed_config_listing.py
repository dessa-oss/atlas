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

        self._local_listing = ConfigListing(f'config/{config_type}')
        self._foundations_listing = ConfigListing(f'{foundations_home()}/config/{config_type}')

    def config_path(self, name):
        return self._local_listing.config_path(name) or self._foundations_listing.config_path(name)