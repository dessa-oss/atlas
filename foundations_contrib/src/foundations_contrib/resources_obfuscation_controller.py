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

    def get_resources(self):
        import shutil
        from foundations_contrib.obfuscator import Obfuscator

        if self.is_obfuscation_activated():
            Obfuscator().obfuscate(self._resource_directory, script='main.py')
            dist_directory = os.path.join(self._resource_directory, 'dist')
            for resource_file in 'run.sh', 'foundations_requirements.txt':
                src_path = os.path.join(self._resource_directory, resource_file)
                dest_path = os.path.join(self._resource_directory, 'dist', resource_file)
                shutil.copyfile(src_path, dest_path)
            return dist_directory
        return self._resource_directory