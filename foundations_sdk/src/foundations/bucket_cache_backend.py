"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class BucketCacheBackend(object):
    def __init__(self, bucket):
        self._bucket = bucket

    def get(self, key):
        object_path = BucketCacheBackend._make_object_path(key)
        return self._get_if_exists(object_path)

    def get_metadata(self, key):
        metadata_path = BucketCacheBackend._make_metadata_path(key)
        return self._get_if_exists(metadata_path)

    def _get_if_exists(self, key):
        if self._bucket.exists(key):
            return self._bucket.download_as_string(key)
        else:
            return None

    def set(self, key, serialized_value, serialized_metadata, **flags):
        object_path = BucketCacheBackend._make_object_path(key)
        metadata_path = BucketCacheBackend._make_metadata_path(key)

        self._bucket.upload_from_string(object_path, serialized_value)
        self._bucket.upload_from_string(metadata_path, serialized_metadata)

    @staticmethod
    def _make_object_path(key):
        return key + "/" + key + ".object"

    @staticmethod
    def _make_metadata_path(key):
        return key + "/" + key + ".metadata"