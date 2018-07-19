"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class PrefixedBucket(object):

    def __init__(self, prefix, bucket_contructor, *constructor_args, **constructor_kwargs):
        self._prefix = prefix
        self._bucket = bucket_contructor(
            *constructor_args, **constructor_kwargs)

    def upload_from_string(self, name, data):
        return self._bucket.upload_from_string(self._name(name), data)

    def upload_from_file(self, name, input_file):
        return self._bucket.upload_from_file(self._name(name), input_file)

    def exists(self, name):
        return self._bucket.exists(self._name(name))

    def download_as_string(self, name):
        return self._bucket.download_as_string(self._name(name))

    def download_to_file(self, name, output_file):
        return self._bucket.download_to_file(self._name(name), output_file)

    def list_files(self, pathname):
        return self._bucket.list_files(self._name(pathname))

    def _name(self, name):
        return self._prefix + '/' + name