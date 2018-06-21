"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ConfigManager(object):

    def __init__(self):
        self._config = None

    def config(self):
        if self._config is None:
            self._load()
        return self._config

    def _load(self):
        from vcat.local_directory import LocalDirectory
        import yaml

        config = {}

        directory = LocalDirectory()
        file_list = directory.get_files('*.config.yaml')
        for bundled_file in file_list:
            with bundled_file.open('r') as file:
                config.update(yaml.load(file))

        self._config = config

    def __getitem__(self, key):
        return self.config()[key]

    def __setitem__(self, key, value):
        self.config()[key] = value

    def reflect_instance(self, name, type_name, default_callback):
        reflected_klass, reflected_args, reflected_kwargs = self.reflect_constructor(
            name, type_name, default_callback)

        return reflected_klass(*reflected_args, **reflected_kwargs)

    def reflect_constructor(self, name, type_name, default_callback):
        config = self.config()
        implementation_key = name + '_implementation'
        if implementation_key in config:
            reflected_implementation = config[implementation_key]
            reflected_klass = reflected_implementation[type_name + '_type']
            reflected_args = reflected_implementation.get(
                'constructor_arguments', [])
            reflected_kwargs = reflected_implementation.get(
                'constructor_keword_arguments', {})
            return reflected_klass, reflected_args, reflected_kwargs
        else:
            return default_callback, [], {}
