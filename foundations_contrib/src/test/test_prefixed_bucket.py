"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_contrib.prefixed_bucket import PrefixedBucket


class TestPrefixedBucket(unittest.TestCase):

    class MockBucket(object):

        def __init__(self):
            self.data = {}

        def upload_from_string(self, name, data):
            self.data[name] = data

        def upload_from_file(self, name, input_file):
            self.data[name] = input_file.read()

        def exists(self, name):
            return name in self.data

        def download_as_string(self, name):
            return self.data.get(name)

        def download_to_file(self, name, output_file):
            value = self.download_as_string(name)
            if value is not None:
                output_file.write(value)
                output_file.flush()
                output_file.seek(0)

        def list_files(self, pathname):
            from fnmatch import fnmatch

            return filter(lambda path: fnmatch(path, pathname), self.data.keys())

        def remove(self, name):
            del self.data[name]

        def move(self, source, destination):
            value = self.download_as_string(source)
            self.remove(source)
            self.upload_from_string(destination, value)

    def setUp(self):
        self._mocked_bucket = self.MockBucket()

    def test_prefixes_string_upload(self):
        bucket = PrefixedBucket('hello', self._mock_bucket)
        bucket.upload_from_string('some_number', 12323)
        self.assertEqual(12323, self._mock_bucket().data['hello/some_number'])

    def test_prefixes_string_upload_different_values(self):
        bucket = PrefixedBucket('goodbye', self._mock_bucket)
        bucket.upload_from_string('some_float', 12.3)
        self.assertEqual(12.3, self._mock_bucket().data['goodbye/some_float'])

    def test_prefixes_existence(self):
        bucket = PrefixedBucket('hello', self._mock_bucket)
        self._mock_bucket().upload_from_string('hello/some_string', 'yup')
        self.assertTrue(bucket.exists('some_string'))

    def test_prefixes_existence_different_values(self):
        bucket = PrefixedBucket('nope', self._mock_bucket)
        self._mock_bucket().upload_from_string('nope/box', 'knife')
        self.assertTrue(bucket.exists('box'))

    def test_prefixes_existence_missing(self):
        bucket = PrefixedBucket('hello', self._mock_bucket)
        self.assertFalse(bucket.exists('some_string'))

    def test_prefixes_existence_missing_different_values(self):
        bucket = PrefixedBucket('nope', self._mock_bucket)
        self.assertFalse(bucket.exists('box'))

    def test_prefixes_file_upload(self):
        bucket = PrefixedBucket('hello', self._mock_bucket)
        with self._make_temp_file() as file:
            file.write_and_flush('potatoes')
            file.seek(0)
            bucket.upload_from_file('some_number', file)
        self.assertEqual(
            'potatoes', self._mock_bucket().data['hello/some_number'])

    def test_prefixes_file_upload_different_values(self):
        bucket = PrefixedBucket('goodbye', self._mock_bucket)
        with self._make_temp_file() as file:
            file.write_and_flush('hello')
            file.seek(0)
            bucket.upload_from_file('some_float', file)
        self.assertEqual(
            'hello', self._mock_bucket().data['goodbye/some_float'])

    def test_prefixes_string_download(self):
        bucket = PrefixedBucket('hello', self._mock_bucket)
        self._mock_bucket().upload_from_string('hello/some_number', 12323)
        self.assertEqual(12323, bucket.download_as_string('some_number'))

    def test_prefixes_string_download_different_values(self):
        bucket = PrefixedBucket('nope', self._mock_bucket)
        self._mock_bucket().upload_from_string('nope/some_string', 'yup')
        self.assertEqual('yup', bucket.download_as_string('some_string'))

    def test_prefixes_file_download(self):
        bucket = PrefixedBucket('nope', self._mock_bucket)
        self._mock_bucket().upload_from_string('nope/some_string', 'yup')
        with self._make_temp_file() as file:
            bucket.download_to_file('some_string', file)
            self.assertEqual('yup', file.read())

    def test_prefixes_file_download_different_values(self):
        bucket = PrefixedBucket('plastic', self._mock_bucket)
        self._mock_bucket().upload_from_string('plastic/bags', 'are dangerous')
        with self._make_temp_file() as file:
            bucket.download_to_file('bags', file)
            self.assertEqual('are dangerous', file.read())

    def test_list_files(self):
        bucket = PrefixedBucket('hello', self._mock_bucket)
        self._mock_bucket().upload_from_string('hello/a', 'b')
        self._mock_bucket().upload_from_string('hello/c', 'd')
        self.assertEqual(set(['a', 'c']), set(bucket.list_files('*')))

    def test_list_files_different_values(self):
        bucket = PrefixedBucket('hello', self._mock_bucket)
        self._mock_bucket().upload_from_string('hello/a', 'b')
        self._mock_bucket().upload_from_string('hello/c', 'd')
        self._mock_bucket().upload_from_string('hello/d', 'd')
        self._mock_bucket().upload_from_string('hello/dead', 'd')
        self.assertEqual(set(['d', 'dead']), set(bucket.list_files('d*')))

    def test_removes_file(self):
        bucket = PrefixedBucket('hello', self._mock_bucket)
        bucket.upload_from_string('some_number', 12323)
        bucket.remove('some_number')
        self.assertFalse(bucket.exists('some_number'))

    def test_removes_file_different_values(self):
        bucket = PrefixedBucket('dunno', self._mock_bucket)
        bucket.upload_from_string('some_other_number', 12323)
        bucket.remove('some_other_number')
        self.assertFalse(bucket.exists('some_other_number'))

    def test_moves_file(self):
        bucket = PrefixedBucket('hello', self._mock_bucket)
        bucket.upload_from_string('some_number', 12323)
        bucket.move('some_number', 'some_other_number')
        self.assertEqual(12323, bucket.download_as_string('some_other_number'))

    def test_moves_file_different_name(self):
        bucket = PrefixedBucket('also_dunno', self._mock_bucket)
        bucket.upload_from_string('some_float', 12.33)
        bucket.move('some_float', 'some_other_float')
        self.assertEqual(12.33, bucket.download_as_string('some_other_float'))

    def _mock_bucket(self):
        return self._mocked_bucket

    def _make_temp_file(self):
        from foundations_contrib.simple_tempfile import SimpleTempfile
        return SimpleTempfile('w+')
