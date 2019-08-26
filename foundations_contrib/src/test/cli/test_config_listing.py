"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from contextlib import contextmanager

class TestConfigListing(Spec):

    @let
    def config_root(self):
        return self.faker.uri_path()

    @let
    def path_listing(self):
        return [f'{self.config_root}/{name}.config.yaml' for name in self.faker.words()]
    
    @let
    def config_listing(self):
        from foundations_contrib.cli.config_listing import ConfigListing
        return ConfigListing(self.config_root)

    @let
    def config_data(self):
        return self.faker.pydict()

    @let
    def yaml_config_data(self):
        import yaml
        return yaml.dump(self.config_data)

    @let
    def mock_listdir(self):
        return ConditionalReturn()

    mock_open = let_patch_mock_with_conditional_return('builtins.open')
    mock_file = let_mock()

    @set_up
    def set_up(self):
        self.mock_listdir.return_when(self.path_listing, f'{self.config_root}/*.config.yaml')
        self.patch('os.listdir', self.mock_listdir)
        self.mock_file.__enter__ = lambda *args: self.mock_file
        self.mock_file.__exit__ = lambda *args: None
        self.mock_file.read.return_value = self.yaml_config_data

    def test_config_list_returns_file_listing_in_config_directory(self):
        listing = self.config_listing.config_list()
        self.assertEqual(self.path_listing, listing)

    def test_config_path_returns_true_if_config_in_path(self):
        self.path_listing.clear()
        self.path_listing.append('/path/to/my/file.config.yaml')
        self.assertEqual('/path/to/my/file.config.yaml', self.config_listing.config_path('file'))

    def test_config_path_returns_false_if_config_not_in_path(self):
        self.assertEqual(None, self.config_listing.config_path('file'))

    def test_config_path_returns_false_if_config_only_partially_in_path(self):
        self.path_listing.clear()
        self.path_listing.append('/path/to/not/my_file.config.yaml')
        self.assertEqual(None, self.config_listing.config_path('file'))

    def test_config_data_returns_yaml_deserialized_config(self):
        self.path_listing.clear()
        self.path_listing.append('/path/to/my/file.config.yaml')
        self.mock_open.return_when(self.mock_file, '/path/to/my/file.config.yaml', 'r')
        self.assertEqual(self.config_data, self.config_listing.config_data('file'))

    def test_config_data_raises_error_when_config_missing(self):
        error_environment = self.faker.sentence()
        with self.assertRaises(ValueError) as error_context:
            self.config_listing.config_data(error_environment)
        self.assertIn(f'No environment {error_environment} found, please set a valid deployment environment with foundations.set_environment', error_context.exception.args[0])
