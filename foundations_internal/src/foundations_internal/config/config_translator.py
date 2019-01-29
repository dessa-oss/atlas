"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ConfigTranslator(object):
    
    def __init__(self):
        self._translators = {}

    def add_translator(self, name, translator):
        self._translators[name] = translator
        
    def translate(self, source_config):
        deployment_type = source_config.get('job_deployment_env', 'local')

        if deployment_type in self._translators:
            return self._translators[deployment_type].translate(source_config)

        raise self._invalid_environment_error(source_config, deployment_type)

    def _invalid_environment_error(self, source_config, deployment_type):
        error_message = 'Got invalid deployment environment `{}`'.format(deployment_type)
        return ValueError(error_message)
