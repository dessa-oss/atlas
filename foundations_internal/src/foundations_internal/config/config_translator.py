"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ConfigTranslator(object):
    
    def __init__(self):
        pass
        
    def translate(self, source_config):
        deployment_type = source_config['job_deployment_env']
        raise self._invalid_environment_error(source_config, deployment_type)

    def _invalid_environment_error(self, source_config, deployment_type):
        error_message = 'Got invalid deployment environment `{}`'.format(deployment_type)
        return ValueError(error_message)
