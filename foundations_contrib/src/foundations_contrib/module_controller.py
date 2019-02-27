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

        if self._is_remote_deployment() and self._need_obfuscation():
            return self._create_obfuscator_generator()
        return module_manager.module_directories_and_names()

    def _is_remote_deployment(self):
        from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment
        return self._config['deployment_implementation']['deployment_type'] != LocalShellJobDeployment
    
    def _need_obfuscation(self):
        return self._config.get('obfuscate', False)
    
    def _create_obfuscator_generator(self):
        from foundations.global_state import module_manager
        from foundations_contrib.obfuscator import Obfuscator

        for module_name, module_directory in module_manager.module_directories_and_names():
            for obfuscated_directory in Obfuscator().obfuscate_all(module_directory):
                yield 'fake stuff', obfuscated_directory
