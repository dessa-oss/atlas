"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations.config_manager import ConfigManager
from mock import patch

from foundations_internal.testing.helpers import let, let_patch_mock
from foundations_internal.testing.helpers.spec import Spec

class TestConfigManager(Spec):

    @let
    def config_manager(self):
        return ConfigManager()

    @let
    def config(self):
        return self.config_manager.config()    

    def test_config_returns_empty(self):
        config = ConfigManager().config()
        self.assertEqual({}, config)

    def test_persist_config(self):
        config_manager = ConfigManager()
        config_manager.config()['hello'] = 'goodbye'
        self.assertEqual({'hello': 'goodbye'}, config_manager.config())

    def test_persist_config_with_different_values(self):
        config_manager = ConfigManager()
        config_manager.config()['foo'] = 'bar'
        self.assertEqual({'foo': 'bar'}, config_manager.config())

    def test_load_config_from_yaml(self):
        from foundations_contrib.change_directory import ChangeDirectory

        with ChangeDirectory('test/fixtures/single_config'):
            config = ConfigManager().config()
            self.assertEqual(
                {'title': 'test config', 'value': 'this exists as a test'}, config)

    def test_load_multiple_config_from_yaml(self):
        from foundations_contrib.change_directory import ChangeDirectory

        with ChangeDirectory('test/fixtures/multiple_configs'):
            config = ConfigManager().config()
            self.assertEqual(
                {'title': 'test config', 'value': 'different value'}, config)

    def test_add_config_path(self):
        config_manager = ConfigManager()
        config_manager.add_config_path(
            'test/fixtures/multiple_configs/second.config.yaml')
        config = config_manager.config()
        self.assertEqual({'value': 'different value'}, config)

    config_translator = let_patch_mock('foundations_internal.global_state.config_translator')

    def test_add_simple_config_path_uses_translated_config(self):
        self.config_translator.translate.return_value = {'some configuration': 'some value for the configuration'}
        self.config_manager.add_simple_config_path('test/fixtures/multiple_configs/first.config.yaml')
        self.config_translator.translate.assert_called_with({'title': 'test config'})
        self.assertEqual({'some configuration': 'some value for the configuration'}, self.config)

    def test_add_simple_config_path_uses_translated_config_different_config(self):
        self.config_translator.translate.return_value = {'some different configuration': 'a value of great importance'}
        self.config_manager.add_simple_config_path('test/fixtures/multiple_configs/second.config.yaml')
        self.config_translator.translate.assert_called_with({'value': 'different value'})
        self.assertEqual({'some different configuration': 'a value of great importance'}, self.config)

    def test_add_config_path_after_configured(self):
        config_manager = ConfigManager()
        config_manager.add_config_path(
            'test/fixtures/multiple_configs/first.config.yaml')
        config = config_manager.config()
        config_manager.add_config_path(
            'test/fixtures/multiple_configs/second.config.yaml')
        self.assertEqual(
            {'title': 'test config', 'value': 'different value'}, config)

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
        self.assertEqual({'hello': 'goodbye'}, config_manager.config())

    def test_config_returns_copy_after_freeze(self):
        config_manager = ConfigManager()
        config_manager['hello'] = 'goodbye'
        config_manager.freeze()
        config_manager.config()['second'] = 'changed thing'
        self.assertEqual({'hello': 'goodbye'}, config_manager.config())

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
