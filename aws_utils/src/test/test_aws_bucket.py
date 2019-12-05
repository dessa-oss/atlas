"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_spec import *

from foundations_aws.aws_bucket import AWSBucket

class TestAWSBucket(Spec):

    class MockListing(object):

        def __init__(self, bucket, files):
            self._bucket = bucket
            self._files = files

        def __call__(self, Bucket, Prefix, Delimiter):
            if Bucket != self._bucket:
                return {}
            return {
                'Contents': [{'Key': Prefix + key} for key in self._grouped_and_prefixed_files(Prefix, Delimiter)],
                'CommonPrefixes': [{'Prefix': Prefix + new_prefix} for new_prefix in self._unique_delimited_prefixes(Prefix, Delimiter)]
            }

        def _unique_delimited_prefixes(self, prefix, delimiter):
            items = set()

            # below is done to preserve order
            for key in self._prefixes(prefix, delimiter):
                if not key in items:
                    items.add(key)
                    yield key

        def _prefixes(self, prefix, delimiter):
            for key in self._prefixed_files(prefix):
                if delimiter in key:
                    yield key.split(delimiter)[0]

        def _grouped_and_prefixed_files(self, prefix, delimiter):
            for key in self._prefixed_files(prefix):
                if not delimiter in key:
                    yield key

        def _prefixed_files(self, prefix):
            prefix_length = len(prefix)
            for key in self._files:
                if key.startswith(prefix):
                    yield key[prefix_length:]

    connection_manager = let_patch_mock(
        'foundations_aws.global_state.connection_manager'
    )
    connection = let_mock()
    mock_file = let_mock()

    @let
    def file_name(self):
        return self.faker.name()

    @let
    def data(self):
        return self.faker.sha256()

    @let
    def data_body(self):
        mock = Mock()
        mock.read.return_value = self.data
        mock.iter_chunks.return_value = [self.data]
        return mock

    @let
    def bucket_prefix(self):
        return self.faker.name()

    @let
    def bucket_postfix(self):
        return self.faker.uri_path()

    @let
    def bucket_name_with_slashes(self):
        return self.bucket_prefix + '/' + self.bucket_postfix

    @let
    def upload_file_name_with_slashes(self):
        return self.bucket_postfix + '/' + self.file_name

    @let
    def bucket(self):
        return AWSBucket(self.bucket_path)

    @let
    def bucket_with_slashes(self):
        return AWSBucket(self.bucket_name_with_slashes)

    @let
    def bucket_path(self):
        return 'testing-bucket'
    
    @let
    def source_path(self):
        return self.faker.name()
    
    @let
    def source_path_with_slashes(self):
        return self.bucket_postfix + '/' + self.source_path

    @set_up
    def set_up(self):
        self.connection_manager.bucket_connection.return_value = self.connection

    def test_upload_from_string_uploads_data_to_bucket_with_prefix(self):
        self.bucket_with_slashes.upload_from_string(self.file_name, self.data)
        self.connection.put_object.assert_called_with(Bucket=self.bucket_prefix, Key=self.upload_file_name_with_slashes, Body=self.data)

    def test_exists_returns_true_when_file_exists_with_prefix(self):
        self.bucket_with_slashes.exists(self.file_name)
        self.connection.head_object.assert_called_with(Bucket=self.bucket_prefix, Key=self.upload_file_name_with_slashes)

    def test_download_as_string_uploads_data_to_bucket_with_prefix(self):
        self.connection.get_object = ConditionalReturn()
        self.connection.get_object.return_when({'Body': self.data_body}, Bucket=self.bucket_prefix, Key=self.upload_file_name_with_slashes)

        result = self.bucket_with_slashes.download_as_string(self.file_name)
        self.assertEqual(self.data, result)
    
    def test_download_to_file_uploads_data_to_bucket_with_prefix(self):
        self.connection.get_object = ConditionalReturn()
        self.connection.get_object.return_when({'Body': self.data_body}, Bucket=self.bucket_prefix, Key=self.upload_file_name_with_slashes)

        result = self.bucket_with_slashes.download_to_file(self.file_name, self.mock_file)
        self.mock_file.write.assert_called_with(self.data)

    def test_remove_removes_prefixed_files(self):
        self.bucket_with_slashes.remove(self.file_name)
        self.connection.delete_object.assert_called_with(Bucket=self.bucket_prefix, Key=self.upload_file_name_with_slashes)

    def test_move_moves_prefixed_files(self):
        self.bucket_with_slashes.move(self.source_path, self.file_name)
        source_info = {'Bucket': self.bucket_prefix, 'Key': self.source_path_with_slashes}
        self.connection.copy_object.assert_called_with(Bucket=self.bucket_prefix, CopySource=source_info, Key=self.upload_file_name_with_slashes)

    def test_list_files_returns_empty(self):
        self.connection.list_objects_v2.side_effect = self.MockListing(
            self.bucket_path,
            []
        )
        self.assertEqual([], self._fetch_listing('*'))

    def test_list_files_returns_all_results(self):
        self.connection.list_objects_v2.side_effect = self.MockListing(
            self.bucket_path,
            ['my.txt', 'scheduler.log']
        )
        self.assertEqual(['my.txt', 'scheduler.log'], self._fetch_listing('*'))

    def test_list_files_returns_file_type_filter(self):
        self.connection.list_objects_v2.side_effect = self.MockListing(
            self.bucket_path,
            ['my.txt', 'scheduler.log']
        )
        self.assertEqual(['my.txt'], self._fetch_listing('*.txt'))

    def test_list_files_returns_all_results_dot_directory(self):
        self.connection.list_objects_v2.side_effect = self.MockListing(
            self.bucket_path,
            ['my.txt', 'scheduler.log']
        )
        self.assertEqual(['my.txt', 'scheduler.log'],
                         self._fetch_listing('./*'))

    def test_list_files_returns_file_type_filter_dot_directory(self):
        self.connection.list_objects_v2.side_effect = self.MockListing(
            self.bucket_path,
            ['my.txt', 'scheduler.log']
        )
        self.assertEqual(['my.txt'], self._fetch_listing('./*.txt'))

    def test_list_files_returns_only_local_directory(self):
        self.connection.list_objects_v2.side_effect = self.MockListing(
            self.bucket_path,
            ['my.txt', 'scheduler.log', 'path/to/some/other/files']
        )
        self.assertEqual(['my.txt', 'scheduler.log', 'path'], self._fetch_listing('*'))

    def test_list_files_returns_only_sub_directory(self):
        self.connection.list_objects_v2.side_effect = self.MockListing(
            self.bucket_path,
            ['my.txt', 'scheduler.log', 'path/to/some/other/files']
        )
        self.assertEqual(['path/to/some/other/files'], self._fetch_listing('path/to/some/other/*'))

    def test_list_files_returns_folder_within_sub_directory(self):
        self.connection.list_objects_v2.side_effect = self.MockListing(
            self.bucket_path,
            ['path/to/some/other/files']
        )
        self.assertEqual(['path/to'], self._fetch_listing('path/*'))

    def test_list_files_returns_arbitrary_filter(self):
        self.connection.list_objects_v2.side_effect = self.MockListing(
            self.bucket_path,
            ['some_stuff_here', 'no_stuff_there', 'some_more_stuff_here']
        )
        self.assertEqual(['some_stuff_here', 'some_more_stuff_here'], self._fetch_listing('some_*_here'))

    def test_list_files_supports_prefixes(self):
        self.connection.list_objects_v2.side_effect = self.MockListing(
            self.bucket_prefix,
            [self.upload_file_name_with_slashes]
        )
        result = list(self.bucket_with_slashes.list_files('*'))
        self.assertEqual([self.file_name], result)

    def _fetch_listing(self, pathname):
        generator = self.bucket.list_files(pathname)
        return list(generator)
