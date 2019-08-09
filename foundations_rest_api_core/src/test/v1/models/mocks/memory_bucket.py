"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class MemoryBucket(object):

    def __init__(self):
        self._bucket = {}

    def upload_from_string(self, name, data):
        self._bucket[name] = data

    def upload_from_file(self, name, input_file):
        self._bucket[name] = input_file.read()

    def exists(self, name):
        return name in self._bucket

    def download_as_string(self, name):
        return self._bucket[name]

    def download_to_file(self, name, output_file):
        output_file.write(self._bucket[name])
        output_file.flush()
        output_file.seek(0)

    def list_files(self, pathname):
        return self._bucket.keys()

    def remove(self, name):
        del self._bucket[name]

    def move(self, source, destination):
        value = self.download_as_string(source)
        self.remove(source)
        self.upload_from_string(destination, value)
