"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec.helpers import let

class ConfigTranslates(object):
    
    @let
    def _configuration(self):
        return {
            'results_config': {
                'archive_end_point': '',
            },
            'cache_config': {
                'end_point': '',
            },
        }

    @let
    def _archive_types(self):
        return [
            'artifact_archive_implementation',
            'job_source_archive_implementation',
            'miscellaneous_archive_implementation',
            'persisted_data_archive_implementation',
            'provenance_archive_implementation',
            'stage_log_archive_implementation',
        ]
    
    def test_returns_archive_listing_configurations_with_local_type(self):
        self._configuration['results_config']['archive_end_point'] = '/path/to/foundations/home'
        result_config = self.translator.translate(self._configuration)
        config = result_config['archive_listing_implementation']
        self.assertEqual(config['archive_listing_type'], self.listing_type)

    def test_returns_project_listing_configurations_with_local_type(self):
        result_config = self.translator.translate(self._configuration)
        config = result_config['project_listing_implementation']
        self.assertEqual(config['project_listing_type'], self.listing_type)

    def test_returns_default_redis_url(self):
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['redis_url'], 'redis://localhost:6379')

    def test_returns_configured_redis_url(self):
        self._configuration['results_config']['redis_end_point'] = 'redis://11.22.33.44:9738'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['redis_url'], 'redis://11.22.33.44:9738')

    def test_returns_cache_configurations_with_local_type(self):
        result_config = self.translator.translate(self._configuration)
        config = result_config['cache_implementation']
        self.assertEqual(config['cache_type'], self.cache_type)

    @let
    def shell_command(self):
        return self.patch('foundations_contrib.helpers.shell.find_bash')

    def test_returns_shell_command(self):
        self.shell_command.return_value = '/path/to/bash'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['shell_command'], '/path/to/bash')

    def test_returns_shell_command_different_command(self):
        self.shell_command.return_value = 'C:\\path\\to\\bash'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['shell_command'], 'C:\\path\\to\\bash')

    def test_returns_obfuscate_false_if_not_set(self):
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['obfuscate_foundations'], False)

    def test_returns_obfuscate_true_if_set_true(self):
        self._configuration['obfuscate_foundations'] = True
        result_config = self.translator.translate(self._configuration)
        self.assertTrue(result_config['obfuscate_foundations'])
    
    def test_returns_obfuscate_false_if_set_false(self):
        self._configuration['obfuscate_foundations'] = False
        result_config = self.translator.translate(self._configuration)
        self.assertFalse(result_config['obfuscate_foundations'])
    
    def test_returns_run_script_environment_with_log_level_same_as_local_log_level(self):
        self._configuration['log_level'] = 'DEBUG'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['run_script_environment']['log_level'], 'DEBUG')
    
    def test_returns_run_script_environment_with_log_level_same_as_local_log_level_different_level(self):
        self._configuration['log_level'] = 'INFO'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['run_script_environment']['log_level'], 'INFO')