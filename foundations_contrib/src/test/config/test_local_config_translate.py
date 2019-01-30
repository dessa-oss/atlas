"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let
from foundations_internal.testing.shared_examples.config_translates import ConfigTranslates

class TestLocalConfigTranslate(Spec, ConfigTranslates):

    @let
    def translator(self):
        import foundations_contrib.config.local_config_translate as translator
        return translator

    @let
    def archive_type(self):
        from foundations_contrib.local_file_system_pipeline_archive import LocalFileSystemPipelineArchive
        return LocalFileSystemPipelineArchive

    @let
    def listing_type(self):
        from foundations_contrib.local_file_system_pipeline_listing import LocalFileSystemPipelineListing
        return LocalFileSystemPipelineListing

    @let
    def cache_type(self):
        from foundations_contrib.local_file_system_cache_backend import LocalFileSystemCacheBackend
        return LocalFileSystemCacheBackend

    def test_returns_archive_configurations_with_provided_path(self):
        self._configuration['results_config']['archive_end_point'] = '/path/to/foundations/home'
        result_config = self.translator.translate(self._configuration)
        for archive_type in self._archive_types:
            config = result_config[archive_type]
            self.assertEqual(config['constructor_arguments'], ['/path/to/foundations/home/archive'])

    def test_returns_archive_configurations_with_provided_path_different_path(self):
        self._configuration['results_config']['archive_end_point'] = '/Users/ml-developer/projects'
        result_config = self.translator.translate(self._configuration)
        for archive_type in self._archive_types:
            config = result_config[archive_type]
            self.assertEqual(config['constructor_arguments'], ['/Users/ml-developer/projects/archive'])

    def test_returns_archive_listing_configuration_with_provided_path(self):
        self._configuration['results_config']['archive_end_point'] = '/path/to/foundations/home'
        result_config = self.translator.translate(self._configuration)
        config = result_config['archive_listing_implementation']
        self.assertEqual(config['constructor_arguments'], ['/path/to/foundations/home/archive'])

    def test_returns_archive_listing_configuration_with_provided_path_different_path(self):
        self._configuration['results_config']['archive_end_point'] = '/Users/ml-developer/projects'
        result_config = self.translator.translate(self._configuration)
        config = result_config['archive_listing_implementation']
        self.assertEqual(config['constructor_arguments'], ['/Users/ml-developer/projects/archive'])

    def test_returns_deployment_with_local_type(self):
        from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment

        result_config = self.translator.translate(self._configuration)
        config = result_config['deployment_implementation']
        self.assertEqual(config['deployment_type'], LocalShellJobDeployment)

    def test_returns_project_listing_configuration_with_provided_path(self):
        self._configuration['results_config']['archive_end_point'] = '/path/to/foundations/home'
        result_config = self.translator.translate(self._configuration)
        config = result_config['project_listing_implementation']
        self.assertEqual(config['constructor_arguments'], ['/path/to/foundations/home/projects'])

    def test_returns_project_listing_configuration_with_provided_path_different_path(self):
        self._configuration['results_config']['archive_end_point'] = '/Users/ml-developer'
        result_config = self.translator.translate(self._configuration)
        config = result_config['project_listing_implementation']
        self.assertEqual(config['constructor_arguments'], ['/Users/ml-developer/projects'])

    def test_returns_cache_configuration_with_provided_path(self):
        self._configuration['cache_config']['end_point'] = '/path/to/foundations/home'
        result_config = self.translator.translate(self._configuration)
        config = result_config['cache_implementation']
        self.assertEqual(config['constructor_arguments'], ['/path/to/foundations/home/cache'])

    def test_returns_cache_configuration_with_provided_path_different_path(self):
        self._configuration['cache_config']['end_point'] = '/Users/ml-developer'
        result_config = self.translator.translate(self._configuration)
        config = result_config['cache_implementation']
        self.assertEqual(config['constructor_arguments'], ['/Users/ml-developer/cache'])

    def test_returns_log_level_configured_to_default(self):
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['log_level'], 'INFO')

    def test_returns_log_level_configured(self):
        self._configuration['log_level'] = 'DEBUG'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['log_level'], 'DEBUG')
