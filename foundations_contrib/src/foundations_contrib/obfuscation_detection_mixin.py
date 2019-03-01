"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ObfuscationDetectionMixin(object):

    def is_obfuscation_activated(self):
        return self._obfuscation_set() and self._is_remote_deployment()        

    def _is_remote_deployment(self):
        from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment
        return self._config['deployment_implementation']['deployment_type'] != LocalShellJobDeployment
    
    def _obfuscation_set(self):
        return self._config['obfuscate_foundations']