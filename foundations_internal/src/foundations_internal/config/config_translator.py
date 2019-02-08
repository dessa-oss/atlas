"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ConfigTranslator(object):
    
    def __init__(self):
        from collections import OrderedDict
        self._translators = OrderedDict()

    def add_translator(self, name, translator):
        self._translators[name] = translator
        
    def translate(self, source_config):
        deployment_type = source_config.get('job_deployment_env', 'local')

        self._load_additional_module_if_necessary(deployment_type)

        if not deployment_type in self._translators:
            raise self._invalid_environment_error(source_config, deployment_type)

        return self._translators[deployment_type].translate(source_config)

    def _load_additional_module_if_necessary(self, deployment_type):
        if not deployment_type in self._translators:
            try:
                from importlib import import_module
                import_module('foundations_{}'.format(deployment_type))
            except ImportError:
                pass

    def _invalid_environment_error(self, source_config, deployment_type):
        supported_deployments = str.join(', ', self._translators)
        error_message = 'Invalid `job_deployment_env` value `{}`. Supported `job_deployment_env`s are: <{}>.'.format(deployment_type, supported_deployments)
        return ValueError(error_message)
