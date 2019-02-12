"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

from foundations_contrib.bucket_cache_backend import BucketCacheBackend

class AWSCacheBackend(BucketCacheBackend):

    def __init__(self, bucket):
        from foundations_aws.aws_bucket import AWSBucket

        super(AWSCacheBackend, self).__init__(AWSBucket(bucket))