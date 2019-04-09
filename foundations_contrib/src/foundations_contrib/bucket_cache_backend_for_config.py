"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.bucket_cache_backend import BucketCacheBackend

class BucketCacheBackendForConfig(BucketCacheBackend):
    
    def __init__(self, bucket_klass, *args, **kwargs):
        bucket = bucket_klass(*args, **kwargs)
        super(BucketCacheBackendForConfig, self).__init__(bucket)
