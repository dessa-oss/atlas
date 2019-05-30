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

class TestFoundationsSchedulerConfigTranslate(Spec, ConfigTranslates, TestBucketFromScheme):

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

    @let
    def bucket_type(self):
        from foundations_ssh.deployment_ssh_bucket import DeploymentSSHBucket
        return DeploymentSSHBucket.bucket_from_single_path

    @set_up
    def ssh_set_up(self):
        self._configuration['ssh_config'] = {
            'host': '',
            'key_path': '',
            'code_path': '',
            'result_path': '',
        }

    def test_returns_deployment_with_sftp_type(self):
        from foundations_scheduler_plugin.job_deployment import JobDeployment

        result_config = self.translator.translate(self._configuration)
        config = result_config['deployment_implementation']
        self.assertEqual(config['deployment_type'], JobDeployment)