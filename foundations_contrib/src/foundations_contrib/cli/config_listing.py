"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class ConfigListing(object):
    
    def __init__(self, config_root):
        self._config_root = config_root

    def config_list(self):
        import os
        return os.listdir(f'{self._config_root}/*.config.yaml')

    def has_config(self, name):
        import os.path

        file_name = f'{name}.config.yaml'

        for config in self.config_list():
            if file_name == os.path.basename(config):
                return True
        return False