"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class ConfigManager(object):

    def __init__(self):
        self._config = None
        self._frozen = False
        self._config_paths = []

    def config(self):
        import copy

        if self._config is None:
            self._load()

        if self._frozen:
            return copy.deepcopy(self._config)
        else:
            return self._config

    def add_config_path(self, path):
        self._config_paths.append(path)
        if self._config is not None:
            self._load_config(self._config, path)

    def add_simple_config_path(self, path):
        from foundations_internal.global_state import config_translator

        config = self._load_yaml(path)
        new_config = config_translator.translate(config)
        self.config().update(new_config)

        self._config_paths.append(path)

    def config_paths(self):
        return self._config_paths

    def freeze(self):
        self._frozen = True

    def frozen(self):
        return self._frozen

    def _load(self):
        import yaml

        config = {}

        for path in self._get_config_paths():
            self._load_config(config, path)

        self._config = config

    def _load_yaml(self, path):
        import yaml

        with open(path, 'r') as file:
            return yaml.load(file)

    def _load_config(self, config, path):
        config.update(self._load_yaml(path))

    def _get_config_paths(self):
        if len(self._config_paths) < 1:
            self._config_paths = self._default_config_paths()

        return self._config_paths

    def _default_config_paths(self):
        from glob import glob
        return glob('*.config.yaml')

    def __getitem__(self, key):
        return self.config()[key]

    def __setitem__(self, key, value):
        if self._frozen:
            self._log().debug('Unable to set {} to {} due to frozen configuration'.format(key, value))
        else:
            self.config()[key] = value
            self._log().debug('Setting {} to {}'.format(key, value))

    def reflect_instance(self, name, type_name, default_callback):
        reflected_klass, reflected_args, reflected_kwargs = self.reflect_constructor(
            name, type_name, default_callback)

        return reflected_klass(*reflected_args, **reflected_kwargs)

    @staticmethod
    def _string_to_type(type_as_string):
        from pydoc import locate
        from foundations.utils import is_string

        if is_string(type_as_string):
            return locate(type_as_string)
        else:
            return type_as_string

    def reflect_constructor(self, name, type_name, default_callback):
        config = self.config()
        implementation_key = name + '_implementation'
        implementation_type = type_name + '_type'
        self._log().debug('Reflecting constructor for {} ({}) via {} ({})'.format(
            name, type_name, implementation_key, implementation_type))
        if implementation_key in config:
            reflected_implementation = config[implementation_key]
            if implementation_key == 'deployment_implementation':
                self._log().info('Configured with {}'.format(reflected_implementation))
            else:
                self._log().debug('Configured with {}'.format(reflected_implementation))

            reflected_klass_string = reflected_implementation[implementation_type]
            reflected_klass = ConfigManager._string_to_type(
                reflected_klass_string)
            reflected_args = reflected_implementation.get(
                'constructor_arguments', [])
            reflected_kwargs = reflected_implementation.get(
                'constructor_keyword_arguments', {})
            return reflected_klass, reflected_args, reflected_kwargs
        else:
            self._log().debug('Returning {}, {}, {}'.format(default_callback, [], {}))
            return default_callback, [], {}

    def _log(self):
        from foundations.global_state import log_manager
        return log_manager.get_logger(__name__)
