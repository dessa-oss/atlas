"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class ModuleController(object):

    def __init__(self, config):
        self._config = config
    
    def get_foundations_modules(self):
        from foundations.global_state import module_manager

        return module_manager.module_directories_and_names()

    def _is_remote_deployment(self):
        from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment
        return self._config['deployment_implementation']['deployment_type'] == LocalShellJobDeployment
