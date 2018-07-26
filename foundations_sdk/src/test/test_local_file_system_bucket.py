"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations.local_file_system_bucket import LocalFileSystemBucket


class TestLocalFileSystemBucket(unittest.TestCase):

    def test_string_upload(self):
        path = self._make_path()
        bucket = self._create_bucket(path)
        bucket.upload_from_string('some_number', '12323')
        with self._open_bucket_file(path, 'some_number') as file:
            self.assertEqual('12323', file.read())

    def test_string_upload_different_values(self):
        path = self._make_path()
        bucket = self._create_bucket(path)
        bucket.upload_from_string('some_float', '12.3')
        with self._open_bucket_file(path, 'some_float') as file:
            self.assertEqual('12.3', file.read())

    def test_existence(self):
        path = self._make_path()
        bucket = self._create_bucket(path)
        bucket.upload_from_string('some_float', '12.3')
        self.assertTrue(bucket.exists('some_float'))

    def test_existence_different_values(self):
        path = self._make_path()
        bucket = self._create_bucket(path)
        bucket.upload_from_string('dunno', 'uno')
        self.assertTrue(bucket.exists('dunno'))

    def test_existence_missing(self):
        path = self._make_path()
        bucket = self._create_bucket(path)
        self.assertFalse(bucket.exists('some_string'))

    def test_existence_missing_different_values(self):
        path = self._make_path()
        bucket = self._create_bucket(path)
        self.assertFalse(bucket.exists('box'))

    def test_file_upload(self):
        path = self._make_path()
        bucket = self._create_bucket(path)
        with self._make_temp_file() as file:
            file.write_and_flush('potatoes')
            file.seek(0)
            bucket.upload_from_file('some_number', file)
        with self._open_bucket_file(path, 'some_number') as file:
            self.assertEqual('potatoes', file.read())

    def test_file_upload_different_values(self):
        path = self._make_path()
        bucket = self._create_bucket(path)
        with self._make_temp_file() as file:
            file.write_and_flush('hello')
            file.seek(0)
            bucket.upload_from_file('some_float', file)
        with self._open_bucket_file(path, 'some_float') as file:
            self.assertEqual('hello', file.read())

    def test_string_download(self):
        path = self._make_path()
        bucket = self._create_bucket(path)
        bucket.upload_from_string('some_number', '12323')
        self.assertEqual('12323', bucket.download_as_string('some_number'))

    def test_string_download_different_values(self):
        path = self._make_path()
        bucket = self._create_bucket(path)
        bucket.upload_from_string('some_string', 'yup')
        self.assertEqual('yup', bucket.download_as_string('some_string'))

    def test_file_download(self):
        path = self._make_path()
        bucket = self._create_bucket(path)
        bucket.upload_from_string('some_string', 'yup')
        with self._make_temp_file() as file:
            bucket.download_to_file('some_string', file)
            self.assertEqual('yup', file.read())

    def test_file_download_different_values(self):
        path = self._make_path()
        bucket = self._create_bucket(path)
        bucket.upload_from_string('bags', 'are dangerous')
        with self._make_temp_file() as file:
            bucket.download_to_file('bags', file)
            self.assertEqual('are dangerous', file.read())

    def test_list_files(self):
        path = self._make_path()
        bucket = self._create_bucket(path)
        bucket.upload_from_string('a', 'b')
        bucket.upload_from_string('c', 'd')
        self.assertEqual(set(['a', 'c']), set(bucket.list_files('*')))

    def test_list_files_different_values(self):
        path = self._make_path()
        bucket = self._create_bucket(path)
        bucket.upload_from_string('a', 'b')
        bucket.upload_from_string('c', 'd')
        bucket.upload_from_string('d', 'd')
        bucket.upload_from_string('dead', 'd')
        self.assertEqual(set(['d', 'dead']), set(bucket.list_files('d*')))

    def test_removes_file(self):
        path = self._make_path()
        bucket = self._create_bucket(path)
        bucket.upload_from_string('some_number', '12323')
        bucket.remove('some_number')
        self.assertFalse(bucket.exists('some_number'))

    def test_removes_file_different_values(self):
        path = self._make_path()
        bucket = self._create_bucket(path)
        bucket.upload_from_string('some_other_number', '12323')
        bucket.remove('some_other_number')
        self.assertFalse(bucket.exists('some_other_number'))

    def test_moves_file(self):
        path = self._make_path()
        bucket = self._create_bucket(path)
        bucket.upload_from_string('some_number', '12323')
        bucket.move('some_number', 'some_other_number')
        self.assertEqual('12323', bucket.download_as_string('some_other_number'))

    def test_moves_file_different_name(self):
        path = self._make_path()
        bucket = self._create_bucket(path)
        bucket.upload_from_string('some_float', '12.33')
        bucket.move('some_float', 'some_other_float')
        self.assertEqual('12.33', bucket.download_as_string('some_other_float'))

    def _open_bucket_file(self, path, name):
        from os.path import join
        return open(join(path, name), 'r')

    def _make_path(self):
        from uuid import uuid4
        return '/tmp/{}'.format(uuid4())

    def _create_bucket(self, path):
        return LocalFileSystemBucket(path)

    def _make_temp_file(self):
        from foundations.simple_tempfile import SimpleTempfile
        return SimpleTempfile('w+')