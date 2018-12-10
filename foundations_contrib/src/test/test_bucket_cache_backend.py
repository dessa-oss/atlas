"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_contrib.bucket_cache_backend import BucketCacheBackend


class TestBucketCacheBackend(unittest.TestCase):
    def setUp(self):
        self.bucket = MockBucket()
        self.backend = BucketCacheBackend(self.bucket)

    def test_get_key_does_not_exist(self):
        self.assertIsNone(self.backend.get("asdf"))

    def test_get_key_object_exists_empty_metadata(self):
        object_path = MockBucket.make_object_path("test")
        metadata_path = MockBucket.make_metadata_path("test")

        self.bucket.upload_from_string(object_path, b"test_value")
        self.bucket.upload_from_string(metadata_path, b"")

        self.assertEqual(self.backend.get("test"), b"test_value")
        self.assertEqual(self.backend.get_metadata("test"), b"")

    def test_get_key_different_object_exists_empty_metadata(self):
        object_path = MockBucket.make_object_path("test")
        metadata_path = MockBucket.make_metadata_path("test")

        self.bucket.upload_from_string(object_path, b"test_value2")
        self.bucket.upload_from_string(metadata_path, b"")

        self.assertEqual(self.backend.get("test"), b"test_value2")
        self.assertEqual(self.backend.get_metadata("test"), b"")

    def test_get_key_different_key_empty_metadata(self):
        object_path = MockBucket.make_object_path("test2")
        metadata_path = MockBucket.make_metadata_path("test2")

        self.bucket.upload_from_string(object_path, b"test_value3")
        self.bucket.upload_from_string(metadata_path, b"")

        self.assertEqual(self.backend.get("test2"), b"test_value3")
        self.assertEqual(self.backend.get_metadata("test2"), b"")

    def test_get_key_wrong_key_empty_metadata(self):
        object_path = MockBucket.make_object_path("test2")
        metadata_path = MockBucket.make_metadata_path("test2")

        self.bucket.upload_from_string(object_path, b"test_value3")
        self.bucket.upload_from_string(metadata_path, b"")

        self.assertIsNone(self.backend.get("test"))
        self.assertIsNone(self.backend.get_metadata("test"))

    def test_get_key_populated_metadata(self):
        object_path = MockBucket.make_object_path("test2")
        metadata_path = MockBucket.make_metadata_path("test2")

        self.bucket.upload_from_string(object_path, b"test_value3")
        self.bucket.upload_from_string(metadata_path, b"asdf")

        self.assertEqual(self.backend.get("test2"), b"test_value3")
        self.assertEqual(self.backend.get_metadata("test2"), b"asdf")

    def test_get_key_different_populated_metadata(self):
        object_path = MockBucket.make_object_path("test2")
        metadata_path = MockBucket.make_metadata_path("test2")

        self.bucket.upload_from_string(object_path, b"test_value3")
        self.bucket.upload_from_string(metadata_path, b"fda")

        self.assertEqual(self.backend.get("test2"), b"test_value3")
        self.assertEqual(self.backend.get_metadata("test2"), b"fda")

    def test_set_correct_paths(self):
        self.backend.set("asdf", b"value", b"")

        self.assertTrue(self.bucket.exists("asdf/asdf.object"))
        self.assertTrue(self.bucket.exists("asdf/asdf.metadata"))

    def test_set_correct_paths_different_key(self):
        self.backend.set("asdf2", b"value", b"")

        self.assertTrue(self.bucket.exists("asdf2/asdf2.object"))
        self.assertTrue(self.bucket.exists("asdf2/asdf2.metadata"))

    def test_set_correct_value(self):
        self.backend.set("asdf", b"value", b"")
        self.assertEqual(self.bucket.download_as_string(
            "asdf/asdf.object"), b"value")

    def test_set_correct_different_value(self):
        self.backend.set("asdf", b"value2", b"")
        self.assertEqual(self.bucket.download_as_string(
            "asdf/asdf.object"), b"value2")

    def test_set_correct_metadata(self):
        self.backend.set("asdf", b"value", b"asdfasdf")
        self.assertEqual(self.bucket.download_as_string(
            "asdf/asdf.metadata"), b"asdfasdf")

    def test_set_correct_different_metadata(self):
        self.backend.set("asdf", b"value", b"asdf")
        self.assertEqual(self.bucket.download_as_string(
            "asdf/asdf.metadata"), b"asdf")

    def test_round_trip(self):
        self.backend.set("asdf", b"value", b"asdf")
        self.assertEqual(self.backend.get("asdf"), b"value")
        self.assertEqual(self.backend.get_metadata("asdf"), b"asdf")


class MockBucket(object):
    def __init__(self):
        self._store = {}

    def exists(self, key):
        return key in self._store

    def upload_from_string(self, key, value):
        self._store[key] = value

    def download_as_string(self, key):
        return self._store.get(key)

    @staticmethod
    def make_object_path(key):
        return key + "/" + key + ".object"

    @staticmethod
    def make_metadata_path(key):
        return key + "/" + key + ".metadata"
