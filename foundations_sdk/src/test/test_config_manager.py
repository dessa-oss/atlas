"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
  
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
        from foundations.change_directory import ChangeDirectory

        with ChangeDirectory('test/fixtures/single_config'):
            config = ConfigManager().config()
            self.assertEqual({'title': 'test config', 'value': 'this exists as a test'}, config)

    def test_load_multiple_config_from_yaml(self):
        from foundations.change_directory import ChangeDirectory

        with ChangeDirectory('test/fixtures/multiple_configs'):
            config = ConfigManager().config()
            self.assertEqual({'title': 'test config', 'value': 'different value'}, config)

    def test_add_config_path(self):
        config_manager = ConfigManager()
        config_manager.add_config_path('test/fixtures/multiple_configs/second.config.yaml')
        config = config_manager.config()
        self.assertEqual({'value': 'different value'}, config)

    def test_add_config_path_after_configured(self):
        config_manager = ConfigManager()
        config_manager.add_config_path('test/fixtures/multiple_configs/first.config.yaml')
        config = config_manager.config()
        config_manager.add_config_path('test/fixtures/multiple_configs/second.config.yaml')
        self.assertEqual({'title': 'test config', 'value': 'different value'}, config)

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
