"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class ModuleObfuscationController(object):

    def __init__(self, config):
        self._config = config
    
    def get_foundations_modules(self):
        from foundations.global_state import module_manager

        if self._is_remote_deployment() and self._need_obfuscation():
            yield from self._create_obfuscator_generator()
        else: 
            yield from module_manager.module_directories_and_names()

    def _is_remote_deployment(self):
        from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment
        return self._config['deployment_implementation']['deployment_type'] != LocalShellJobDeployment
    
    def _need_obfuscation(self):
        return self._config.get('obfuscate_foundations', False)
        
    def _create_obfuscator_generator(self):
        from foundations.global_state import module_manager
        from foundations_contrib.obfuscator import Obfuscator

        obfuscator = Obfuscator()
        for module_name, module_root_directory in module_manager.module_directories_and_names():
            for obfuscated_absolute_dist_directory in obfuscator.obfuscate_all(module_root_directory):
                relative_module_path = self._generate_relative_path(module_name, module_root_directory, obfuscated_absolute_dist_directory)
                yield relative_module_path, obfuscated_absolute_dist_directory

    def _generate_relative_path(self, module_name, module_root_directory, obfuscated_absolute_dist_directory):
        import os

        absolute_child_directory = os.path.dirname(obfuscated_absolute_dist_directory)

        if absolute_child_directory == module_root_directory:
            return module_name

        module_root_directory = os.path.join(module_root_directory, '')
        remaining_path = absolute_child_directory.split(module_root_directory, 1)[-1]
        return os.path.join(module_name, remaining_path)
