"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class BucketPipelineListing(object):

    def __init__(self, bucket_constructor, *constructor_args, **constructor_kwargs):
        self._bucket = bucket_constructor(
            *constructor_args, **constructor_kwargs)

    def track_pipeline(self, pipeline_name):
        self._bucket.upload_from_string(
            pipeline_name + '.tracker', pipeline_name)

    def get_pipeline_names(self):
        from foundations.utils import string_from_bytes
        from foundations.helpers.future import Future

        file_names = self._bucket.list_files('*.tracker')
        def get_pipeline_name(name):
            byte_file_names = self._bucket.download_as_string(name)
            return string_from_bytes(byte_file_names)

        futures = [Future.execute(get_pipeline_name, name) for name in file_names]
        return Future.all(futures).get()
