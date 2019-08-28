"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_internal.testing.shared_examples.config_translates import ConfigTranslates
from foundations_internal.testing.shared_examples.test_bucket_from_scheme import TestBucketFromScheme


from foundations_ssh.deployment_ssh_bucket import DeploymentSSHBucket

class TestScheduler(Spec):

    @let
    def _configuration(self):
        return {
            'results_config': {},
            'ssh_config': {
                'host': '',
                'key_path': '',
                'code_path': '',
                'result_path': '',
            }
        }

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
    def translator(self):
        import foundations_scheduler_plugin.config.scheduler as translator
        return translator

    @let
    def archive_type(self):
        from foundations_contrib.bucket_pipeline_archive import BucketPipelineArchive
        return BucketPipelineArchive

    @let
    def listing_type(self):
        from foundations.bucket_pipeline_listing import BucketPipelineListing
        return BucketPipelineListing

    @let
    def cache_type(self):
        from foundations_contrib.local_file_system_cache_backend import LocalFileSystemCacheBackend
        return LocalFileSystemCacheBackend

    @let
    def bucket_type(self):
        from foundations_ssh.deployment_ssh_bucket import DeploymentSSHBucket
        return DeploymentSSHBucket.bucket_from_single_path
        
    @let
    def shell_command(self):
        return self.patch('foundations_contrib.helpers.shell.find_bash')

    @let
    def worker_config(self):
        return self.faker.pydict()

    def test_returns_default_redis_url(self):
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['redis_url'], 'redis://localhost:6379')

    def test_returns_configured_redis_url(self):
        self._configuration['results_config']['redis_end_point'] = 'redis://11.22.33.44:9738'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['redis_url'], 'redis://11.22.33.44:9738')

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

    def test_returns_deployment_with_sftp_type(self):
        from foundations_scheduler_plugin.job_deployment import JobDeployment

        result_config = self.translator.translate(self._configuration)
        config = result_config['deployment_implementation']
        self.assertEqual(config['deployment_type'], JobDeployment)

    def test_config_translator_can_take_worker_config_and_return_translated_config(self):
        self._configuration['worker'] = self.worker_config
        result_config = self.translator.translate(self._configuration)
        worker_overrides = result_config['worker_container_overrides']
        self.assertEqual(self.worker_config, worker_overrides)

    def test_config_translator_has_empty_worker_config(self):
        result_config = self.translator.translate(self._configuration)
        worker_overrides = result_config['worker_container_overrides']
        self.assertEqual({}, worker_overrides)
