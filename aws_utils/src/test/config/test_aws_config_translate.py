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

class TestAWSConfigTranslate(Spec, ConfigTranslates, TestBucketFromScheme):

    @let
    def translator(self):
        import foundations_aws.config.aws_config_translate as translator
        return translator

    @let
    def archive_type(self):
        from foundations_aws.aws_pipeline_archive import AWSPipelineArchive
        return AWSPipelineArchive

    @let
    def listing_type(self):
        from foundations_aws.aws_pipeline_archive_listing import AWSPipelineArchiveListing
        return AWSPipelineArchiveListing

    @let
    def cache_type(self):
        from foundations_aws.aws_cache_backend import AWSCacheBackend
        return AWSCacheBackend

    @let
    def bucket_type(self):
        from foundations_aws.aws_bucket import AWSBucket
        return AWSBucket

    @set_up
    def set_up(self):
        self._configuration['ssh_config'] = {
            'host': '',
            'key_path': '',
            'code_path': '',
            'result_path': '',
        }

    def test_returns_deployment_with_local_type(self):
        from foundations_ssh.sftp_job_deployment import SFTPJobDeployment

        result_config = self.translator.translate(self._configuration)
        config = result_config['deployment_implementation']
        self.assertEqual(config['deployment_type'], SFTPJobDeployment)

    def test_no_result_artifact_returns_constructor_arguments_with_default_artifact_path(self):
        from foundations_aws.aws_bucket import AWSBucket

        result_config = self.translator.translate(self._configuration)
        config = result_config['artifact_end_point_implementation']
        self.assertEqual([AWSBucket, 'results'], config['constructor_arguments'])

    def test_missing_artifact_end_point_returns_constructor_arguments_with_aws_bucket(self):
        from foundations_aws.aws_bucket import AWSBucket

        self._configuration['results_config']['artifact_path'] = self.fake_relative_path
        result_config = self.translator.translate(self._configuration)
        config = result_config['artifact_end_point_implementation']
        self.assertEqual([AWSBucket, self.fake_relative_path], config['constructor_arguments'])
