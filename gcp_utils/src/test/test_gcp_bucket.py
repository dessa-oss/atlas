"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers.conditional_return import ConditionalReturn
from foundations_internal.testing.helpers import let, let_now, let_patch_mock, let_patch_instance, set_up, let_mock
from foundations_gcp.gcp_bucket import GCPBucket

class TestGCPBucket(Spec):

    bucket_connection = let_patch_instance('foundations_gcp.global_state.connection_manager.bucket_connection')
    bucket = let_mock()
    blob = let_mock()

    @let
    def faker(self):
        from faker import Faker
        return Faker()

    @let
    def file_name(self):
        return self.faker.name()

    @let
    def bucket_name(self):
        return self.faker.name()

    @let
    def data(self):
        return self.faker.sha256()

    @let
    def gcp_bucket(self):
        return GCPBucket(self.bucket_name)

    @set_up
    def set_up(self):
        self.bucket_connection.get_bucket = ConditionalReturn()
        self.bucket_connection.get_bucket.return_when(self.bucket, self.bucket_name)
        self.bucket.blob = ConditionalReturn()
        self.bucket.blob.return_when(self.blob, self.file_name)
    
    def test_upload_from_string_uploads_data_to_bucket(self):
        self.gcp_bucket.upload_from_string(self.file_name, self.data)
        self.blob.upload_from_string.assert_called_with(self.data)
    
    def test_upload_from_file_uploads_data_to_bucket(self):
        self.gcp_bucket.upload_from_file(self.file_name, self.data)
        self.blob.upload_from_file.assert_called_with(self.data)
    
    def test_exists_calls_blob_exists(self):
        self.gcp_bucket.exists(self.file_name)
        self.blob.exists.assert_called()
    
    def test_exists_returns_true_when_blob_exists_is_true(self):
        self.blob.exists.return_value = True
        self.assertEqual(self.gcp_bucket.exists(self.file_name), True)
