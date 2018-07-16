"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class GCPBucket(object):

    def __init__(self, name):
        from vcat_gcp.global_state import connection_manager

        self._connection = connection_manager.bucket_connection()
        self._bucket = self._connection.get_bucket(name)

    def upload_from_string(self, name, data):
        self._blob(name).upload_from_string(data)

    def upload_from_file(self, name, input_file):
        self._blob(name).upload_from_file(input_file)

    def exists(self, name):
        return self._blob(name).exists()

    def download_as_string(self, name):
        from vcat.utils import byte_string

        data_bytes = self._blob(name).download_as_string()
        return byte_string(data_bytes)

    def download_to_file(self, name, output_file):
        self._blob(name).download_to_file(output_file)
        output_file.flush()
        output_file.seek(0)

    def list_files(self, pathname):
        from os.path import dirname
        from os.path import basename
        from fnmatch import fnmatch

        directory = dirname(pathname)
        path_filter = basename(pathname)

        objects = self._bucket.list_blobs(
            prefix=directory + '/', delimiter='/')
        object_names = [bucket_object.name for bucket_object in objects]
        object_file_names = [basename(path) for path in object_names]
        return filter(lambda path: fnmatch(path, path_filter), object_file_names)
    
    def move(self, source, destination):
        self._blob(source).rename_blob(destination)

    def _blob(self, name):
        return self._bucket.blob(name)
