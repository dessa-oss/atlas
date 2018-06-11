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
        from vcat.local_file_system_bucket import LocalFileSystemBucket

        bucket_path = path or getcwd()
        bucket_path = abspath(bucket_path)
        self._bucket = LocalFileSystemBucket(bucket_path)

    def track_pipeline(self, pipeline_name):
        self._bucket.upload_from_string(pipeline_name + '.tracker', pipeline_name)

    def get_pipeline_names(self):
        file_names = self._bucket.list_files('*.tracker')
        return [self._bucket.download_as_string(name) for name in file_names]