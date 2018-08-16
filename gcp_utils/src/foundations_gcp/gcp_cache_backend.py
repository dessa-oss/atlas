"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class GCPCacheBackend(object):

    def __init__(self, bucket):
        from foundations_gcp.gcp_bucket import GCPBucket

        self._bucket = GCPBucket(bucket)

    def get(self, key):
        if self._bucket.exists(key):
            return self._bucket.download_as_string(key)

    def get_metadata(self, key):
        pass

    def set(self, key, serialized_value, metadata, **flags):
        self._bucket.upload_from_string(key, serialized_value)
