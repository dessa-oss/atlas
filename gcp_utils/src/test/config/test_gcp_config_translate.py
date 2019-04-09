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

class TestGCPConfigTranslate(Spec, ConfigTranslates, TestBucketFromScheme):

    @let
    def translator(self):
        import foundations_gcp.config.gcp_config_translate as translator
        return translator

    @let
    def archive_type(self):
        from foundations_gcp.gcp_pipeline_archive import GCPPipelineArchive
        return GCPPipelineArchive

    @let
    def listing_type(self):
        from foundations_gcp.gcp_pipeline_archive_listing import GCPPipelineArchiveListing
        return GCPPipelineArchiveListing

    @let
    def cache_type(self):
        from foundations_gcp.gcp_cache_backend import GCPCacheBackend
        return GCPCacheBackend
    
    @let
    def bucket_type(self):
        from foundations_gcp.gcp_bucket import GCPBucket
        return GCPBucket

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

    def test_returns_log_level_configured_to_default(self):
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['log_level'], 'INFO')

    def test_returns_log_level_configured(self):
        self._configuration['log_level'] = 'DEBUG'
        result_config = self.translator.translate(self._configuration)
        self.assertEqual(result_config['log_level'], 'DEBUG')

    
