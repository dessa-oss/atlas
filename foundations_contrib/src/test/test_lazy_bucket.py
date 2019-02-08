"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let, let_mock, set_up

class TestLazyBucket(Spec):

    @let
    def lazy_bucket(self):
        from foundations_contrib.lazy_bucket import LazyBucket
        return LazyBucket(self.bucket_constructor)

    @set_up
    def set_up(self):
        self.bucket_constructor.return_value = self.bucket

    bucket_constructor = let_mock()
    bucket = let_mock()    
    name = let_mock()
    data = let_mock()
    input_file = let_mock()
    output_file = let_mock()
    dummy = let_mock()
    pathname = let_mock()
    source = let_mock()
    destination = let_mock()

    def test_ensure_bucket_is_not_constructed(self):
        self.lazy_bucket
        self.bucket_constructor.assert_not_called()

    def test_upload_from_string_calls_bucket(self):
        self.bucket.upload_from_string.return_value = self.dummy
        result = self.lazy_bucket.upload_from_string(self.name, self.data)
        self.bucket.upload_from_string.assert_called_with(self.name, self.data)
        self.assertEqual(self.dummy, result)

    def test_upload_from_file_calls_bucket(self):
        self.bucket.upload_from_file.return_value = self.dummy
        result = self.lazy_bucket.upload_from_file(self.name, self.input_file)
        self.bucket.upload_from_file.assert_called_with(self.name, self.input_file)
        self.assertEqual(self.dummy, result)

    def test_exists_calls_bucket(self):
        self.bucket.exists.return_value = self.dummy
        result = self.lazy_bucket.exists(self.name)
        self.bucket.exists.assert_called_with(self.name)
        self.assertEqual(self.dummy, result)

    def test_download_as_string_calls_bucket(self):
        self.bucket.download_as_string.return_value = self.dummy
        result = self.lazy_bucket.download_as_string(self.name)
        self.bucket.download_as_string.assert_called_with(self.name)
        self.assertEqual(self.dummy, result)

    def test_download_to_file_calls_bucket(self):
        self.bucket.download_to_file.return_value = self.dummy
        result = self.lazy_bucket.download_to_file(self.name, self.output_file)
        self.bucket.download_to_file.assert_called_with(self.name, self.output_file)
        self.assertEqual(self.dummy, result)

    def test_list_files_calls_bucket(self):
        self.bucket.list_files.return_value = self.dummy
        result = self.lazy_bucket.list_files(self.pathname)
        self.bucket.list_files.assert_called_with(self.pathname)
        self.assertEqual(self.dummy, result)

    def test_remove_calls_bucket(self):
        self.bucket.remove.return_value = self.dummy
        result = self.lazy_bucket.remove(self.name)
        self.bucket.remove.assert_called_with(self.name)
        self.assertEqual(self.dummy, result)

    def test_move_calls_bucket(self):
        self.bucket.move.return_value = self.dummy
        result = self.lazy_bucket.move(self.source, self.destination)
        self.bucket.move.assert_called_with(self.source, self.destination)
        self.assertEqual(self.dummy, result)

