"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

import foundations_contrib.config.local_config_translate as translator
from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let

class TestLocalConfigTranslate(Spec):
    
    def setUp(self):
        self._configuration = {
            'results_config': {
                'archive_end_point': '',
            },
            'cache_config': {
                'end_point': '',
            },
        }
        self._archive_types = [
            'artifact_archive_implementation',
            'job_source_archive_implementation',
            'miscellaneous_archive_implementation',
            'persisted_data_archive_implementation',
            'provenance_archive_implementation',
            'stage_log_archive_implementation',
        ]

    def test_returns_archive_configurations_with_provided_path(self):
        self._configuration['results_config']['archive_end_point'] = '/path/to/foundations/home'
        result_config = translator.translate(self._configuration)
        for archive_type in self._archive_types:
            config = result_config[archive_type]
            self.assertEqual(config['constructor_arguments'], ['/path/to/foundations/home/archive'])

    def test_returns_archive_configurations_with_provided_path_different_path(self):
        self._configuration['results_config']['archive_end_point'] = '/Users/ml-developer/projects'
        result_config = translator.translate(self._configuration)
        for archive_type in self._archive_types:
            config = result_config[archive_type]
            self.assertEqual(config['constructor_arguments'], ['/Users/ml-developer/projects/archive'])

    def test_returns_archive_configurations_with_local_type(self):
        from foundations_contrib.local_file_system_pipeline_archive import LocalFileSystemPipelineArchive

        self._configuration['results_config']['archive_end_point'] = '/path/to/foundations/home'
        result_config = translator.translate(self._configuration)
        for archive_type in self._archive_types:
            config = result_config[archive_type]
            self.assertEqual(config['archive_type'], LocalFileSystemPipelineArchive)

    def test_returns_archive_listing_configuration_with_provided_path(self):
        self._configuration['results_config']['archive_end_point'] = '/path/to/foundations/home'
        result_config = translator.translate(self._configuration)
        config = result_config['archive_listing_implementation']
        self.assertEqual(config['constructor_arguments'], ['/path/to/foundations/home/archive'])

    def test_returns_archive_listing_configuration_with_provided_path_different_path(self):
        self._configuration['results_config']['archive_end_point'] = '/Users/ml-developer/projects'
        result_config = translator.translate(self._configuration)
        config = result_config['archive_listing_implementation']
        self.assertEqual(config['constructor_arguments'], ['/Users/ml-developer/projects/archive'])

    def test_returns_archive_listing_configurations_with_local_type(self):
        from foundations_contrib.local_file_system_pipeline_listing import LocalFileSystemPipelineListing

        self._configuration['results_config']['archive_end_point'] = '/path/to/foundations/home'
        result_config = translator.translate(self._configuration)
        config = result_config['archive_listing_implementation']
        self.assertEqual(config['archive_type'], LocalFileSystemPipelineListing)

    def test_returns_deployment_with_local_type(self):
        from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment

        result_config = translator.translate(self._configuration)
        config = result_config['deployment_implementation']
        self.assertEqual(config['deployment_type'], LocalShellJobDeployment)

    def test_returns_project_listing_configuration_with_provided_path(self):
        self._configuration['results_config']['archive_end_point'] = '/path/to/foundations/home'
        result_config = translator.translate(self._configuration)
        config = result_config['project_listing_implementation']
        self.assertEqual(config['constructor_arguments'], ['/path/to/foundations/home/projects'])

    def test_returns_project_listing_configuration_with_provided_path_different_path(self):
        self._configuration['results_config']['archive_end_point'] = '/Users/ml-developer'
        result_config = translator.translate(self._configuration)
        config = result_config['project_listing_implementation']
        self.assertEqual(config['constructor_arguments'], ['/Users/ml-developer/projects'])

    def test_returns_project_listing_configurations_with_local_type(self):
        from foundations_contrib.local_file_system_pipeline_listing import LocalFileSystemPipelineListing

        result_config = translator.translate(self._configuration)
        config = result_config['project_listing_implementation']
        self.assertEqual(config['archive_type'], LocalFileSystemPipelineListing)

    def test_returns_default_redis_url(self):
        result_config = translator.translate(self._configuration)
        self.assertEqual(result_config['redis_url'], 'redis://localhost:6379')

    def test_returns_configured_redis_url(self):
        self._configuration['results_config']['redis_end_point'] = 'redis://11.22.33.44:9738'
        result_config = translator.translate(self._configuration)
        self.assertEqual(result_config['redis_url'], 'redis://11.22.33.44:9738')

    def test_returns_cache_configuration_with_provided_path(self):
        self._configuration['cache_config']['end_point'] = '/path/to/foundations/home'
        result_config = translator.translate(self._configuration)
        config = result_config['cache_implementation']
        self.assertEqual(config['constructor_arguments'], ['/path/to/foundations/home/cache'])

    def test_returns_cache_configuration_with_provided_path_different_path(self):
        self._configuration['cache_config']['end_point'] = '/Users/ml-developer'
        result_config = translator.translate(self._configuration)
        config = result_config['cache_implementation']
        self.assertEqual(config['constructor_arguments'], ['/Users/ml-developer/cache'])

    def test_returns_cache_configurations_with_local_type(self):
        from foundations_contrib.local_file_system_cache_backend import LocalFileSystemCacheBackend

        result_config = translator.translate(self._configuration)
        config = result_config['cache_implementation']
        self.assertEqual(config['cache_type'], LocalFileSystemCacheBackend)

    def test_returns_log_level_configured_to_default(self):
        from foundations_contrib.local_file_system_cache_backend import LocalFileSystemCacheBackend

        result_config = translator.translate(self._configuration)
        self.assertEqual(result_config['log_level'], 'INFO')

    def test_returns_log_level_configured(self):
        from foundations_contrib.local_file_system_cache_backend import LocalFileSystemCacheBackend

        self._configuration['log_level'] = 'DEBUG'
        result_config = translator.translate(self._configuration)
        self.assertEqual(result_config['log_level'], 'DEBUG')

    @let
    def shell_command(self):
        return self.patch('foundations_contrib.helpers.shell.find_bash')

    def test_returns_shell_command(self):
        self.shell_command.return_value = '/path/to/bash'
        result_config = translator.translate(self._configuration)
        self.assertEqual(result_config['shell_command'], '/path/to/bash')

    def test_returns_shell_command_different_command(self):
        self.shell_command.return_value = 'C:\\path\\to\\bash'
        result_config = translator.translate(self._configuration)
        self.assertEqual(result_config['shell_command'], 'C:\\path\\to\\bash')