"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class LazyBucket(object):
    
    def __init__(self, bucket_constructor):
        self._bucket = None
        self._bucket_constructor = bucket_constructor

    def upload_from_string(self, name, data):
        return self._get_bucket().upload_from_string(name, data)

    def upload_from_file(self, name, input_file):
        return self._get_bucket().upload_from_file(name, input_file)

    def exists(self, name):
        return self._get_bucket().exists(name)

    def download_as_string(self, name):
        return self._get_bucket().download_as_string(name)

    def download_to_file(self, name, output_file):
        return self._get_bucket().download_to_file(name, output_file)

    def list_files(self, pathname):
        return self._get_bucket().list_files(pathname)

    def remove(self, name):
        return self._get_bucket().remove(name)

    def move(self, source, destination):
        return self._get_bucket().move(source, destination)
    
    def _get_bucket(self):
        if self._bucket is None:
            self._bucket = self._bucket_constructor()
        return self._bucket