"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import let, set_up
from foundations_internal.testing.shared_examples.config_translates import ConfigTranslates
from foundations_internal.testing.shared_examples.test_bucket_from_scheme import TestBucketFromScheme

from foundations_ssh.deployment_ssh_bucket import DeploymentSSHBucket

class TestSSHConfigTranslate(Spec, ConfigTranslates, TestBucketFromScheme):
    
    @let
    def translator(self):
        import foundations_ssh.config.ssh_config_translate as translator
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

    def test_returns_deployment_with_sftp_type(self):
        from foundations_ssh.sftp_job_deployment import SFTPJobDeployment

        result_config = self.translator.translate(self._configuration)
        config = result_config['deployment_implementation']
        self.assertEqual(config['deployment_type'], SFTPJobDeployment)
