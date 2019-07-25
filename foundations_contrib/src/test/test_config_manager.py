"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations.config_manager import ConfigManager
from mock import patch

class TestConfigManager(Spec):

    mock_file = let_mock()
    
    @let_now
    def mock_os_environ(self):
        return self.patch('os.environ', self.environment)

    @let
    def environment(self):
        return self.faker.pydict()

    @let
    def config_manager(self):
        return ConfigManager()

    @let
    def config(self):
        return self.config_manager.config()    

    @let
    def config_file_path(self):
        return self.faker.file_path()

    @let
    def config_file_path_list(self):
        import random

        path_list_length = random.randint(2, 10)
        path_list = []

        for _ in range(path_list_length):
            path_list.append(self.faker.file_path())

        return path_list

    @let
    def run_script_environment(self):
        return self.faker.pydict()

    @set_up
    def set_up(self):
        self.mock_file.__enter__ = lambda *args: self.mock_file
        self.mock_file.__exit__ = lambda *args: None
        self.mock_file.read.return_value = ''

    def test_should_include_foundations_environment(self):
        config_manager = ConfigManager()
        self.environment['FOUNDATIONS_hello'] = 'world'
        self.assertEqual('world', config_manager['hello'])

    def test_should_include_foundations_environment_with_different_values(self):
        config_manager = ConfigManager()
        self.environment['FOUNDATIONS_world'] = 'hello'
        self.assertEqual('hello', config_manager['world'])

    def test_should_be_empty_by_default(self):
        config_manager = ConfigManager()
        self.assertEqual({'run_script_environment': {}}, config_manager.config())

    def test_persist_config(self):
        config_manager = ConfigManager()
        config_manager.config()['hello'] = 'goodbye'
        self._assert_is_subset({'hello': 'goodbye'}, config_manager.config())

    def test_persist_config_with_different_values(self):
        config_manager = ConfigManager()
        config_manager.config()['foo'] = 'bar'
        self._assert_is_subset({'foo': 'bar'}, config_manager.config())

    def test_load_config_from_yaml(self):
        from foundations_contrib.change_directory import ChangeDirectory

        with ChangeDirectory('test/fixtures/single_config'):
            config = ConfigManager().config()
            self._assert_is_subset(
                {'title': 'test config', 'value': 'this exists as a test'}, config)

    def test_load_multiple_config_from_yaml(self):
        from foundations_contrib.change_directory import ChangeDirectory

        with ChangeDirectory('test/fixtures/multiple_configs'):
            config = ConfigManager().config()
            self._assert_is_subset(
                {'title': 'test config', 'value': 'different value'}, config)

    def test_add_config_path(self):
        config_manager = ConfigManager()
        config_manager.add_config_path(
            'test/fixtures/multiple_configs/second.config.yaml')
        config = config_manager.config()
        self._assert_is_subset({'value': 'different value'}, config)

    config_translator = let_patch_mock('foundations_internal.global_state.config_translator')

    def test_add_simple_config_path_uses_translated_config(self):
        self.config_translator.translate.return_value = {'some configuration': 'some value for the configuration'}
        self.config_manager.add_simple_config_path('test/fixtures/multiple_configs/first.config.yaml')
        self.config_translator.translate.assert_called_with({'title': 'test config'})
        self._assert_is_subset({'some configuration': 'some value for the configuration'}, self.config)

    def test_add_simple_config_path_uses_translated_config_different_config(self):
        self.config_translator.translate.return_value = {'some different configuration': 'a value of great importance'}
        self.config_manager.add_simple_config_path('test/fixtures/multiple_configs/second.config.yaml')
        self.config_translator.translate.assert_called_with({'value': 'different value'})
        self._assert_is_subset({'some different configuration': 'a value of great importance'}, self.config)

    def test_add_config_path_after_configured(self):
        config_manager = ConfigManager()
        config_manager.add_config_path(
            'test/fixtures/multiple_configs/first.config.yaml')
        config = config_manager.config()
        config_manager.add_config_path(
            'test/fixtures/multiple_configs/second.config.yaml')
        self._assert_is_subset(
            {'title': 'test config', 'value': 'different value'}, config)

    def test_config_paths_returns_empty_list_if_no_paths_added(self):
        config_manager = ConfigManager()
        self.assertEqual([], config_manager.config_paths())

    def test_config_paths_returns_singleton_list_with_added_path(self):
        mock_open = self.patch('builtins.open')
        mock_open.return_value = self.mock_file

        config_manager = ConfigManager()
        config_manager.add_simple_config_path(self.config_file_path)
        self.assertEqual([self.config_file_path], config_manager.config_paths())

    def test_config_paths_returns_list_with_added_paths(self):
        mock_open = self.patch('builtins.open')
        mock_open.return_value = self.mock_file

        config_manager = ConfigManager()

        for config_file_path in self.config_file_path_list:
            config_manager.add_simple_config_path(config_file_path)

        self.assertEqual(self.config_file_path_list, config_manager.config_paths())

    def test_indexer(self):
        config_manager = ConfigManager()
        config_manager.config()['hello'] = 'goodbye'
        self.assertEqual('goodbye', config_manager['hello'])

    def test_indexer_different_key(self):
        config_manager = ConfigManager()
        config_manager.config()['next'] = 'thing'
        self.assertEqual('thing', config_manager['next'])

    def test_indexer_multiple_value(self):
        config_manager = ConfigManager()
        config_manager.config()['hello'] = 'goodbye'
        config_manager.config()['next'] = 'thing'
        self.assertEqual('thing', config_manager['next'])

    def test_indexer_assignment_operator(self):
        config_manager = ConfigManager()
        config_manager['hello'] = 'goodbye'
        self.assertEqual('goodbye', config_manager['hello'])

    def test_indexer_assignment_operator_with_different_value(self):
        config_manager = ConfigManager()
        config_manager['cat'] = 'dog'
        self.assertEqual('dog', config_manager['cat'])

    def test_not_frozen(self):
        config_manager = ConfigManager()
        self.assertFalse(config_manager.frozen())

    def test_frozen(self):
        config_manager = ConfigManager()
        config_manager.freeze()
        self.assertTrue(config_manager.frozen())

    def test_config_does_not_persist_after_freeze(self):
        config_manager = ConfigManager()
        config_manager['hello'] = 'goodbye'
        config_manager.freeze()
        config_manager['second'] = 'changed thing'
        self.assertEqual({'hello': 'goodbye', 'run_script_environment': {}}, config_manager.config())

    def test_config_returns_copy_after_freeze(self):
        config_manager = ConfigManager()
        config_manager['hello'] = 'goodbye'
        config_manager.freeze()
        config_manager.config()['second'] = 'changed thing'
        self.assertEqual({'hello': 'goodbye', 'run_script_environment': {}}, config_manager.config())

    def test_reflect_instance_creates_default_implementation(self):
        config_manager = ConfigManager()
        instance = config_manager.reflect_instance(
            'potato', 'tomato', lambda: 'carrot')
        self.assertEqual('carrot', instance)

    def test_reflect_instance_creates_default_implementation_different_default(self):
        config_manager = ConfigManager()
        instance = config_manager.reflect_instance(
            'box', 'cat', lambda: 'socks')
        self.assertEqual('socks', instance)

    def test_reflect_instance_creates_configured_callback(self):
        def MyClass():
            return 'socks'

        config_manager = ConfigManager()
        config_manager['box_implementation'] = {
            'cat_type': MyClass
        }
        instance = config_manager.reflect_instance('box', 'cat', lambda: None)
        self.assertEqual('socks', instance)

    def test_reflect_instance_creates_configured_callback_with_different_type(self):
        def MyClass():
            return 'shorts'

        config_manager = ConfigManager()
        config_manager['cup_implementation'] = {
            'mouse_type': MyClass
        }
        instance = config_manager.reflect_instance(
            'cup', 'mouse', lambda: None)
        self.assertEqual('shorts', instance)

    def test_reflect_instance_creates_configured_callback_with_different_type(self):
        def MyClassTwo():
            return 'two socks'

        config_manager = ConfigManager()
        config_manager['box_implementation'] = {
            'cat_type': MyClassTwo
        }
        instance = config_manager.reflect_instance('box', 'cat', lambda: None)
        self.assertEqual('two socks', instance)

    def test_reflect_instance_creates_configured_callback_with_arguments(self):
        def MyClass(first, second):
            return '{}.{}'.format(first, second)

        config_manager = ConfigManager()
        config_manager['box_implementation'] = {
            'cat_type': MyClass,
            'constructor_arguments': ['hello', 'pippin']
        }
        instance = config_manager.reflect_instance('box', 'cat', lambda: None)
        self.assertEqual('hello.pippin', instance)

    def test_reflect_instance_creates_configured_callback_with_different_arguments(self):
        def MyClass(first, second):
            return '{}.{}'.format(first, second)

        config_manager = ConfigManager()
        config_manager['box_implementation'] = {
            'cat_type': MyClass,
            'constructor_arguments': ['goodbye', 'thomas']
        }
        instance = config_manager.reflect_instance('box', 'cat', lambda: None)
        self.assertEqual('goodbye.thomas', instance)

    def test_reflect_instance_creates_configured_callback_with_keyword_arguments(self):
        def MyClass(first, second):
            return '{} {}'.format(first, second)
        config_manager = ConfigManager()
        config_manager['box_implementation'] = {
            'cat_type': MyClass,
            'constructor_keyword_arguments': {'first': 'i am', 'second': 'a potato'}
        }
        instance = config_manager.reflect_instance('box', 'cat', lambda: None)
        self.assertEqual('i am a potato', instance)

    def test_reflect_instance_creates_configured_callback_with_different_keyword_arguments(self):
        def MyClass(first, second):
            return '{} {}'.format(first, second)

        config_manager = ConfigManager()
        config_manager['box_implementation'] = {
            'cat_type': MyClass,
            'constructor_keyword_arguments': {'first': 'i am not', 'second': 'a good potato'}
        }
        instance = config_manager.reflect_instance('box', 'cat', lambda: None)
        self.assertEqual('i am not a good potato', instance)

    def test_reflect_instance_creates_configured_callback_with_string_type(self):
        config_manager = ConfigManager()
        config_manager['box_implementation'] = {
            'cat_type': 'str',
            'constructor_arguments': ['socks']
        }
        instance = config_manager.reflect_instance('box', 'cat', lambda: None)
        self.assertEqual('socks', instance)
    
    def test_config_manager_get_run_script_environment_defaults_to_empty_dict(self):
        config_manager = ConfigManager()
        self.assertEqual({}, config_manager.config()['run_script_environment'])

    def test_config_manager_run_script_environment_is_not_lost_if_modified_directly(self):
        config_manager = ConfigManager()
        config_manager.config()['run_script_environment'].update(self.run_script_environment)
        self.assertEqual(self.run_script_environment, config_manager.config()['run_script_environment'])

    def call_reflect_constructor(self, metric):
        config_manager = ConfigManager()
        config_manager[metric +
                       '_implementation'] = {metric + '_type': 'some_' + metric}
        config_manager.reflect_constructor(metric, metric, lambda: 'socks')

    @patch('logging.Logger.info')
    def test_reflect_constructor_info(self, mock):
        self.call_reflect_constructor('deployment')
        mock.assert_called_with(
            'Configured with {\'deployment_type\': \'some_deployment\'}')

    @patch('logging.Logger.debug')
    def test_reflect_constructor_debug(self, mock):
        self.call_reflect_constructor('archive')
        mock.assert_called_with(
            'Configured with {\'archive_type\': \'some_archive\'}')

    def _assert_is_subset(self, subset, superset):
        is_not_subset_exception = AssertionError('{} is not a subset of {}'.format(subset, superset))

        for key in subset:
            if key not in superset or subset[key] != superset[key]:
                raise is_not_subset_exception