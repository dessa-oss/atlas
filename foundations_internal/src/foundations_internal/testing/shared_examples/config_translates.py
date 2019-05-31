"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class ConfigTranslates(object):
    
    @let
    def _configuration(self):
        return {
            'results_config': {
                'archive_end_point': '',
                'artifact_path': 'results',
            },
            'cache_config': {
                'end_point': '',
            },
            'ssh_config': {
                'host': '',
                'key_path': '',
                'code_path': '',
                'result_path': '',
            }
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
    
    @let
    def fake_user(self):
        return self.faker.last_name()

    @let
    def fake_ip(self):
        return self.faker.ipv4()

    @let
    def fake_port(self):
        return self.faker.random_number()

    @let
    def fake_key_path(self):
        return self.faker.uri_path()
    
    @let
    def fake_code_path(self):
        return self.faker.uri_path()
    
    @let
    def fake_result_path(self):
        return self.faker.uri_path()
    
    @let
    def fake_artifact_path(self):
        return self.faker.uri_path()

    def test_returns_default_redis_url(self):
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['redis_url'], 'redis://localhost:6379')

    def test_returns_configured_redis_url(self):
        self._configuration['results_config']['redis_end_point'] = 'redis://11.22.33.44:9738'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['redis_url'], 'redis://11.22.33.44:9738')

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

    def test_returns_ssh_user_default_user(self):
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['remote_user'], 'foundations')

    def test_returns_ssh_user(self):
        self._configuration['ssh_config']['user'] = self.fake_user
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['remote_user'], self.fake_user)
    
    def test_returns_host(self):
        self._configuration['ssh_config']['host'] = self.fake_ip
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['remote_host'], self.fake_ip)
    
    def test_returns_port_default_port(self):
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['port'], 22)
    
    def test_returns_port(self):
        self._configuration['ssh_config']['port'] = self.fake_port
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['port'], self.fake_port)
    
    def test_returns_key_path(self):
        self._configuration['ssh_config']['key_path'] = self.fake_key_path
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['key_path'], self.fake_key_path)

    def test_returns_code_path(self):
        self._configuration['ssh_config']['code_path'] = self.fake_code_path
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['code_path'], self.fake_code_path)
    
    def test_returns_result_path(self):
        self._configuration['ssh_config']['result_path'] = self.fake_result_path
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['result_path'], self.fake_result_path)

    def test_returns_log_level_configured_to_default(self):
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['log_level'], 'INFO')

    def test_returns_log_level_configured(self):
        self._configuration['log_level'] = 'DEBUG'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['log_level'], 'DEBUG')

    def test_no_result_artifact_returns_constructor_arguments_with_default_artifact_path(self):
        from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

        self._configuration['artifact_path'] = self.fake_artifact_path
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(self.fake_artifact_path, result_config['artifact_path'])

    def test_no_result_artifact_returns_constructor_arguments_with_default_artifact_path(self):
        from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

        result_config = self.translator.translate(self._configuration)
        self.assertEqual('results', result_config['artifact_path'])

