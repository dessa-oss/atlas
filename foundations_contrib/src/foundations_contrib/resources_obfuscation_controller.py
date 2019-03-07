"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from foundations_contrib.obfuscation_detection_mixin import ObfuscationDetectionMixin
import os

class ResourcesObfuscationController(ObfuscationDetectionMixin):

    def __init__(self, config):
        self._config = config
        self._module_directory = os.path.dirname(os.path.abspath(__file__))
        self._resource_directory = os.path.join(self._module_directory, "resources")
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        from foundations_contrib.obfuscator import Obfuscator
        if self.is_obfuscation_activated():
            Obfuscator().cleanup(self._resource_directory)

    def get_resources(self):
        if self.is_obfuscation_activated():
            return self._get_obfuscated_resources_directory()    
        return self._resource_directory

    def _get_obfuscated_resources_directory(self):
        from foundations_contrib.obfuscator import Obfuscator

        Obfuscator().obfuscate(self._resource_directory, script='main.py')
        for resource_file in 'run.sh', 'foundations_requirements.txt':
            self._copy_file_to_dist_directory(resource_file)
        return os.path.join(self._resource_directory, 'dist')

    def _copy_file_to_dist_directory(self, resource_file):
        import shutil

        src_path = os.path.join(self._resource_directory, resource_file)
        dest_path = os.path.join(self._resource_directory, 'dist', resource_file)
        shutil.copy2(src_path, dest_path)
