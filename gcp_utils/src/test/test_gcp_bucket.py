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
    mock_file = let_mock()

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
    def encoded_data(self):
        return self.data.encode('utf-8')

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
        self.blob.exists.return_value = False
        self.assertFalse(self.gcp_bucket.exists(self.file_name))

    def test_exists_returns_true_when_blob_exists_is_true(self):
        self.blob.exists.return_value = True
        self.assertTrue(self.gcp_bucket.exists(self.file_name))

    def test_download_as_string_returns_data_stored_in_blob(self):
        self.blob.download_as_string.return_value = self.data
        self.assertEqual(self.encoded_data, self.gcp_bucket.download_as_string(self.file_name))

    def test_download_as_string_returns_data_stored_in_blob_when_blob_returns_binary(self):
        self.blob.download_as_string.return_value = self.encoded_data
        self.assertEqual(self.encoded_data, self.gcp_bucket.download_as_string(self.file_name))

    def test_download_to_file_calls_blob_method_with_input_file(self):
        self.gcp_bucket.download_to_file(self.file_name, self.mock_file)
        self.blob.download_to_file.assert_called_with(self.mock_file)

    def test_download_to_file_flushes_file(self):
        self.gcp_bucket.download_to_file(self.file_name, self.mock_file)
        self.mock_file.flush.assert_called()

    def test_download_to_file_rewinds_file(self):
        self.gcp_bucket.download_to_file(self.file_name, self.mock_file)
        self.mock_file.seek.assert_called_with(0)
