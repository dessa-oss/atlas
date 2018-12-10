"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.bucket_cache_backend import BucketCacheBackend


class LocalFileSystemCacheBackend(BucketCacheBackend):

    def __init__(self, path):
        from foundations_contrib.local_file_system_bucket import LocalFileSystemBucket

        super(LocalFileSystemCacheBackend, self).__init__(
            LocalFileSystemBucket(path))
