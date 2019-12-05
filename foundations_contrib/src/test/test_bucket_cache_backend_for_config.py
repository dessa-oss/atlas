"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_contrib.bucket_cache_backend_for_config import BucketCacheBackendForConfig


class TestBucketCacheBackendForConfig(Spec):

    bucket_instance = let_mock()

    @let
    def bucket_klass(self):
        mock = ConditionalReturn()
        mock.return_when(self.bucket_instance, *self.random_args, **self.random_kwargs)
        return mock

    @let
    def random_args(self):
        return self.faker.words()

    @let
    def random_kwargs(self):
        return self.faker.pydict()

    @let
    def cache_backend(self):
        return BucketCacheBackendForConfig(self.bucket_klass, *self.random_args, **self.random_kwargs)

    @let
    def fake_data(self):
        return self.faker.sha1()

    @let
    def fake_metadata(self):
        return self.faker.sha1()

    @let
    def cache_name(self):
        return self.faker.uri_path() + '/does_exist'

    @let
    def cache_object_name(self):
        return self.cache_name + "/" + self.cache_name + ".object"

    @let
    def cache_metadata_name(self):
        return self.cache_name + "/" + self.cache_name + ".metadata"

    @let
    def cache_does_not_exist_name(self):
        return self.faker.uri_path() + '/does_not_exist'

    @let
    def cache_object_does_not_exist_name(self):
        return self.cache_does_not_exist_name + "/" + self.cache_does_not_exist_name + ".object"

    @let
    def cache_metadata_does_not_exist_name(self):
        return self.cache_does_not_exist_name + "/" + self.cache_does_not_exist_name + ".metadata"

    @set_up
    def set_up(self):
        self.bucket_instance.download_as_string = ConditionalReturn()
        self.bucket_instance.download_as_string.return_when(self.fake_data, self.cache_object_name)
        self.bucket_instance.download_as_string.return_when(self.fake_metadata, self.cache_metadata_name)
        self.bucket_instance.exists = ConditionalReturn()
        self.bucket_instance.exists.return_when(False, self.cache_object_does_not_exist_name)
        self.bucket_instance.exists.return_when(False, self.cache_metadata_does_not_exist_name)
        self.bucket_instance.exists.return_when(True, self.cache_metadata_name)
        self.bucket_instance.exists.return_when(True, self.cache_object_name)

    def test_get_returns_underlying_bucket_data(self):
        self.assertEqual(self.fake_data, self.cache_backend.get(self.cache_name))
    
    def test_get_key_object_exists_empty_metadata(self):
        self.assertEqual(self.fake_metadata, self.cache_backend.get_metadata(self.cache_name))
    
    def test_get_returns_empty_metadata_when_key_does_not_exist_in_bucket(self):
        self.assertIsNone(self.cache_backend.get_metadata(self.cache_does_not_exist_name))

    def test_get_returns_empty_data_when_key_does_not_exist_in_bucket(self):
        self.assertIsNone(self.cache_backend.get(self.cache_does_not_exist_name))

    def test_set_sets_object_when_called(self):
        self.cache_backend.set(self.cache_name, self.fake_data, self.fake_metadata)
        self.bucket_instance.upload_from_string.assert_any_call(self.cache_object_name, self.fake_data)
    
    def test_set_sets_metadata_when_called(self):
        self.cache_backend.set(self.cache_name, self.fake_data, self.fake_metadata)
        self.bucket_instance.upload_from_string.assert_any_call(self.cache_metadata_name, self.fake_metadata)
    
