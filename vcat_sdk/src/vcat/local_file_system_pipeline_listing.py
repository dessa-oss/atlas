"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class LocalFileSystemPipelineListing(object):

    def __init__(self, path=None):
        from os import getcwd
        from os.path import abspath
        from vcat.bucket_pipeline_listing import BucketPipelineListing
        from vcat.local_file_system_bucket import LocalFileSystemBucket

        bucket_path = path or getcwd()
        bucket_path = abspath(bucket_path)
        self._listing = BucketPipelineListing(LocalFileSystemBucket, bucket_path)

    def track_pipeline(self, pipeline_name):
        return self._listing.track_pipeline(pipeline_name)

    def get_pipeline_names(self):
        return self._listing.get_pipeline_names()