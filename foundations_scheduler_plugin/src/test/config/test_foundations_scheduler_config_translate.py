"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_internal.testing.shared_examples.config_translates import ConfigTranslates

from foundations_ssh.deployment_ssh_bucket import DeploymentSSHBucket

class TestFoundationsSchedulerConfigTranslate(Spec, ConfigTranslates):
    
    @let
    def translator(self):
        import foundations_scheduler_plugin.config.foundations_scheduler_config_translate as translator
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

    @set_up
    def ssh_set_up(self):
        self._configuration['ssh_config'] = {
            'host': '',
            'key_path': '',
            'code_path': '',
            'result_path': '',
        }

    def test_returns_archive_configurations_with_provided_path(self):
        self._configuration['results_config']['archive_end_point'] = '/path/to/foundations/home'
        result_config = self.translator.translate(self._configuration)
        for archive_type in self._archive_types:
            config = result_config[archive_type]
            self.assertEqual(config['constructor_arguments'], [DeploymentSSHBucket, '/path/to/foundations/home/archive', '/path/to/foundations/home/archive'])

    def test_returns_archive_configurations_with_provided_path_different_path(self):
        self._configuration['results_config']['archive_end_point'] = '/Users/ml-developer/projects'
        result_config = self.translator.translate(self._configuration)
        for archive_type in self._archive_types:
            config = result_config[archive_type]
            self.assertEqual(config['constructor_arguments'], [DeploymentSSHBucket, '/Users/ml-developer/projects/archive', '/Users/ml-developer/projects/archive'])

    def test_returns_archive_listing_configuration_with_provided_path(self):
        self._configuration['results_config']['archive_end_point'] = '/path/to/foundations/home'
        result_config = self.translator.translate(self._configuration)
        config = result_config['archive_listing_implementation']
        self.assertEqual(config['constructor_arguments'], [DeploymentSSHBucket, '/path/to/foundations/home/archive', '/path/to/foundations/home/archive'])

    def test_returns_archive_listing_configuration_with_provided_path_different_path(self):
        self._configuration['results_config']['archive_end_point'] = '/Users/ml-developer/projects'
        result_config = self.translator.translate(self._configuration)
        config = result_config['archive_listing_implementation']
        self.assertEqual(config['constructor_arguments'], [DeploymentSSHBucket, '/Users/ml-developer/projects/archive', '/Users/ml-developer/projects/archive'])

    def test_returns_deployment_with_sftp_type(self):
        from foundations_ssh.sftp_job_deployment import SFTPJobDeployment

        result_config = self.translator.translate(self._configuration)
        config = result_config['deployment_implementation']
        self.assertEqual(config['deployment_type'], SFTPJobDeployment)

    def test_returns_project_listing_configuration_with_provided_path(self):
        self._configuration['results_config']['archive_end_point'] = '/path/to/foundations/home'
        result_config = self.translator.translate(self._configuration)
        config = result_config['project_listing_implementation']
        self.assertEqual(config['constructor_arguments'], [DeploymentSSHBucket, '/path/to/foundations/home/projects', '/path/to/foundations/home/projects'])

    def test_returns_project_listing_configuration_with_provided_path_different_path(self):
        self._configuration['results_config']['archive_end_point'] = '/Users/ml-developer'
        result_config = self.translator.translate(self._configuration)
        config = result_config['project_listing_implementation']
        self.assertEqual(config['constructor_arguments'], [DeploymentSSHBucket, '/Users/ml-developer/projects', '/Users/ml-developer/projects'])

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

    def test_returns_ssh_user_default_user(self):
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['remote_user'], 'foundations')
    
    def test_returns_ssh_user(self):
        self._configuration['ssh_config']['user'] = 'whoami'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['remote_user'], 'whoami')
    
    def test_returns_ssh_user_different_user(self):
        self._configuration['ssh_config']['user'] = 'whoareyou'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['remote_user'], 'whoareyou')
    
    def test_returns_host(self):
        self._configuration['ssh_config']['host'] = '11.22.33.44'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['remote_host'], '11.22.33.44')
    
    def test_returns_host_different_host(self):
        self._configuration['ssh_config']['host'] = '7.9.8.10'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['remote_host'], '7.9.8.10')
    
    def test_returns_port_default_port(self):
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['port'], 22)
    
    def test_returns_port(self):
        self._configuration['ssh_config']['port'] = 12233
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['port'], 12233)
    
    def test_returns_port_different_port(self):
        self._configuration['ssh_config']['port'] = 14233
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['port'], 14233)
    
    def test_returns_key_path(self):
        self._configuration['ssh_config']['key_path'] = '/home/lou/.ssh/id_rsa'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['key_path'], '/home/lou/.ssh/id_rsa')
    
    def test_returns_key_path_different_key_path(self):
        self._configuration['ssh_config']['key_path'] = '/home/hana/.ssh/id_dev'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['key_path'], '/home/hana/.ssh/id_dev')
    
    def test_returns_code_path(self):
        self._configuration['ssh_config']['code_path'] = '/home/foundations/foundations-scheduler/code'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['code_path'], '/home/foundations/foundations-scheduler/code')
    
    def test_returns_code_path_different_code_path(self):
        self._configuration['ssh_config']['code_path'] = '/home/foundations/scheduler/code'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['code_path'], '/home/foundations/scheduler/code')
    
    def test_returns_result_path(self):
        self._configuration['ssh_config']['result_path'] = '/home/foundations/foundations-scheduler/result'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['result_path'], '/home/foundations/foundations-scheduler/result')
    
    def test_returns_result_path_different_result_path(self):
        self._configuration['ssh_config']['result_path'] = '/home/foundations/scheduler/result'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['result_path'], '/home/foundations/scheduler/result')

