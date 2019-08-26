"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestConfigListing(Spec):

    @let
    def config_root(self):
        return self.faker.uri_path()

    @let
    def path_listing(self):
        return [self.config_root + '/' + name for name in self.faker.words()]
    
    @let
    def config_listing(self):
        from foundations_contrib.cli.config_listing import ConfigListing
        return ConfigListing(self.config_root)

    @let
    def mock_listdir(self):
        return ConditionalReturn()

    @set_up
    def set_up(self):
        self.mock_listdir.return_when(self.path_listing, f'{self.config_root}/*.config.yaml')
        self.patch('os.listdir', self.mock_listdir)

    def test_config_list_returns_file_listing_in_config_directory(self):
        listing = self.config_listing.config_list()
        self.assertEqual(self.path_listing, listing)

    def test_has_config_returns_true_if_config_in_path(self):
        self.path_listing.clear()
        self.path_listing.append('/path/to/my/file.config.yaml')
        self.assertEqual(True, self.config_listing.has_config('file'))

    def test_has_config_returns_false_if_config_not_in_path(self):
        self.assertEqual(False, self.config_listing.has_config('file'))

    def test_has_config_returns_false_if_config_only_partially_in_path(self):
        self.path_listing.clear()
        self.path_listing.append('/path/to/not/my_file.config.yaml')
        self.assertEqual(False, self.config_listing.has_config('file'))
