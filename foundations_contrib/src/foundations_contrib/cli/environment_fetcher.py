"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class EnvironmentFetcher(object):
    """
    Checks the local and global config locations for environments
    """

    def __init__(self):
        pass
    
    def get_all_environments(self):
        local_environments = self._get_local_environments()

        global_environments = self._get_global_environments()

        if local_environments != "Wrong directory":
            return local_environments + global_environments
        return global_environments
    
    def find_environment(self, env_name):
        file_name = '{}.{}'.format(env_name, 'config.yaml')
        local_environments = self._get_local_environments()

        if local_environments == "Wrong directory":
            return local_environments
        global_environments = self._get_global_environments()
        all_environments = local_environments + global_environments
        return [env for env in all_environments if file_name in env]


    def _get_local_environments(self):
        import os
        from glob import glob

        cwd = os.getcwd()
        directories = os.listdir()

        if 'config' not in directories:
            return "Wrong directory" 

        config_directory = '{}/{}/{}'.format(cwd, 'config', '*.config.yaml')
        return glob(config_directory)
        
    
    def _get_global_environments(self):
        from glob import glob
        from os.path import expanduser
        global_config_directory = expanduser('~/.foundations/config')
        search_path = '{}/{}'.format(global_config_directory, '*.config.yaml')
        return glob(search_path)
