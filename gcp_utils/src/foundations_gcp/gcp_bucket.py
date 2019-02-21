"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class GCPBucket(object):

    def __init__(self, name):
        from foundations_gcp.global_state import connection_manager
        import traceback

        split_name = name.split('/', 1)
        self._bucket_name = split_name[0]

        if len(split_name) > 1:
            self._bucket_postfix = split_name[1] + '/'
        else:
            self._bucket_postfix = ''

        self._bucket = connection_manager.bucket_connection().get_bucket(self._bucket_name)

    def upload_from_string(self, name, data):
        self._blob(name).upload_from_string(data)

    def upload_from_file(self, name, input_file):
        self._blob(name).upload_from_file(input_file)

    def exists(self, name):
        return self._blob(name).exists()

    def download_as_string(self, name):
        from foundations.utils import byte_string

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
        prefix = self._list_files_prefix(directory)
        path_filter = basename(pathname)

        objects = self._bucket.list_blobs(prefix=prefix, delimiter='/')
        object_names = [bucket_object.name for bucket_object in objects]
        object_file_names = [basename(path) for path in object_names]
        for path in object_file_names:
            if fnmatch(path, path_filter):
                yield '{}/{}'.format(directory, path)

    def _list_files_prefix(self, directory):
        from os.path import join
        
        if self._bucket_postfix:
            prefix = self._bucket_postfix
            if directory:
                prefix += directory + '/'
        else:
            prefix = directory + '/'
        return prefix

    def remove(self, name):
        self._log().debug('Removing {}'.format(name))
        self._blob(name).delete()

    def move(self, source, destination):
        blob = self._blob(source)
        self._bucket.rename_blob(blob, destination)

    def _blob(self, name):
        return self._bucket.blob(self._bucket_postfix + name)

    def _log(self):
        from foundations.global_state import log_manager
        return log_manager.get_logger(__name__)
