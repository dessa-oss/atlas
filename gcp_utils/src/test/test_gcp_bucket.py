"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers.conditional_return import ConditionalReturn
from foundations_spec.helpers import let, let_now, let_patch_mock, let_patch_instance, set_up, let_mock
from foundations_gcp.gcp_bucket import GCPBucket

class TestGCPBucket(Spec):

    bucket_connection = let_patch_instance('foundations_gcp.global_state.connection_manager.bucket_connection')
    bucket = let_mock()
    blob = let_mock()
    mock_file = let_mock()

    @let
    def file_name(self):
        return self.faker.name()

    @let
    def upload_file_name(self):
        return self.file_name

    @let
    def other_file_name(self):
        return self.faker.name()

    @let
    def bucket_name(self):
        return self.faker.name()

    @let
    def bucket_prefix(self):
        return self.faker.name()

    @let
    def bucket_postfix(self):
        return self.faker.name()

    @let
    def bucket_postfix_two(self):
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
        self.bucket.blob.return_when(self.blob, self.upload_file_name)
        self.bucket.list_blobs = ConditionalReturn()

    def test_upload_from_string_uploads_data_to_bucket(self):
        self.gcp_bucket.upload_from_string(self.file_name, self.data)
        self.blob.upload_from_string.assert_called_with(self.data)

    def test_upload_from_string_uploads_data_to_bucket_with_prefix(self):
        bucket_name = self.bucket_prefix + '/' + self.bucket_postfix
        upload_file_name = self.bucket_postfix + '/' + self.file_name
        
        self.bucket_connection.get_bucket.clear()
        self.bucket_connection.get_bucket.return_when(self.bucket, self.bucket_prefix)
        self.bucket.blob.clear()
        self.bucket.blob.return_when(self.blob, upload_file_name)

        gcp_bucket = GCPBucket(bucket_name)

        gcp_bucket.upload_from_string(self.file_name, self.data)
        self.blob.upload_from_string.assert_called_with(self.data)

    def test_upload_from_string_uploads_data_to_bucket_with_long_prefix(self):
        bucket_name = self.bucket_prefix + '/' + self.bucket_postfix + '/' + self.bucket_postfix_two
        upload_file_name = self.bucket_postfix + '/' + self.bucket_postfix_two + '/' + self.file_name
        
        self.bucket_connection.get_bucket.clear()
        self.bucket_connection.get_bucket.return_when(self.bucket, self.bucket_prefix)
        self.bucket.blob.clear()
        self.bucket.blob.return_when(self.blob, upload_file_name)

        gcp_bucket = GCPBucket(bucket_name)

        gcp_bucket.upload_from_string(self.file_name, self.data)
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

    def test_remove_calls_remove_on_the_blob(self):
        self.gcp_bucket.remove(self.file_name)
        self.blob.delete.assert_called()

    def test_move_calls_rename_on_the_blob_with_new_filename(self):
        self.gcp_bucket.move(self.file_name, self.other_file_name)
        self.bucket.rename_blob.assert_called_with(self.blob, self.other_file_name)

    def test_list_files_returns_no_files_when_bucket_is_empty(self):
        self._mock_list_blobs([])
        self.assertEqual([], list(self.gcp_bucket.list_files('*')))

    def test_list_files_returns_a_single_file(self):
        self._mock_list_blobs([
            self._create_mock_object(self.file_name)
        ])
        result = list(self.gcp_bucket.list_files('*'))
        expected_result = ['/' + self.file_name]
        self.assertEqual(expected_result, result)

    def test_list_files_returns_multiple_files(self):
        self._mock_list_blobs([
            self._create_mock_object(self.file_name),
            self._create_mock_object(self.other_file_name)
        ])
        result = list(self.gcp_bucket.list_files('*'))
        expected_result = [
            '/' + self.file_name,
            '/' + self.other_file_name
        ]
        self.assertEqual(expected_result, result)    

    def test_list_files_returns_filters_files(self):
        self._mock_list_blobs([
            self._create_mock_object('file_one'),
            self._create_mock_object('file_two')
        ])
        result = list(self.gcp_bucket.list_files('file_one'))
        expected_result = [
            '/file_one'
        ]
        self.assertEqual(expected_result, result)
    
    def test_list_files_returns_filters_files_with_bucket_prefix(self):
        bucket_name = self.bucket_prefix + '/' + self.bucket_postfix
        
        self.bucket_connection.get_bucket.clear()
        self.bucket_connection.get_bucket.return_when(self.bucket, self.bucket_prefix)

        gcp_bucket = GCPBucket(bucket_name)
        self._mock_list_blobs([
            self._create_mock_object(self.bucket_postfix + '/file_one'),
            self._create_mock_object(self.bucket_postfix + '/file_two')
        ], prefix=self.bucket_postfix + '/')
        result = list(gcp_bucket.list_files('file_one'))
        expected_result = [
            '/file_one'
        ]
        self.assertEqual(expected_result, result)
    
    def test_list_files_returns_a_single_file_relative_to_path(self):
        self._mock_list_blobs([
            self._create_mock_object('some/path/file_one.txt')
            ], 
            prefix='some/path/'
        )
        result = list(self.gcp_bucket.list_files('some/path/*'))
        expected_result = ['some/path/file_one.txt']
        self.assertEqual(expected_result, result)
    
    def test_list_files_returns_filters_files_with_bucket_prefix_and_path_prefix(self):
        bucket_name = self.bucket_prefix + '/' + self.bucket_postfix
        
        self.bucket_connection.get_bucket.clear()
        self.bucket_connection.get_bucket.return_when(self.bucket, self.bucket_prefix)

        gcp_bucket = GCPBucket(bucket_name)
        self._mock_list_blobs([
            self._create_mock_object(self.bucket_postfix + '/some/path/file_one.txt')
        ], prefix=self.bucket_postfix + '/some/path/')
        result = list(gcp_bucket.list_files('some/path/*'))
        expected_result = [
            'some/path/file_one.txt'
        ]
        self.assertEqual(expected_result, result)

    def test_list_files_returns_filters_files_on_file_extension(self):
        self._mock_list_blobs([
            self._create_mock_object('file_one.txt'),
            self._create_mock_object('file_two.exe')
        ])
        result = list(self.gcp_bucket.list_files('*.exe'))
        expected_result = [
            '/file_two.exe'
        ]
        self.assertEqual(expected_result, result)

    def _create_mock_object(self, name):
        mock = Mock()
        mock.name = name
        return mock

    def _mock_list_blobs(self, blobs_return_value, prefix='/'):
        self.bucket.list_blobs.return_when(
            blobs_return_value,
            prefix=prefix, delimiter='/'
        )
