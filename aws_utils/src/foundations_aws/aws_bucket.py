"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

##### Rework entire file

class AWSBucket(object):

    def __init__(self, name):
        from foundations_aws.global_state import connection_manager

        self._connection = connection_manager.bucket_connection()
        self._bucket_name = name

    def upload_from_string(self, name, data):
        pass

    def upload_from_file(self, name, input_file):
        pass

    def exists(self, name):
        pass

    def download_as_string(self, name):
        pass

    def download_to_file(self, name, output_file):
        pass

    def list_files(self, pathname):
        # from os.path import dirname
        # from os.path import basename
        # from fnmatch import fnmatch

        # directory = dirname(pathname)
        # path_filter = basename(pathname)

        # objects = self._bucket.list_blobs(
        #     prefix=directory + '/', delimiter='/')
        # object_names = [bucket_object.name for bucket_object in objects]
        # object_file_names = [basename(path) for path in object_names]
        # for path in object_file_names:
        #     if fnmatch(path, path_filter):
        #         yield '{}/{}'.format(directory, path)

    def remove(self, name):
        pass
    
    def move(self, source, destination):
        pass

    def _blob(self, name):
        pass

    def _log(self):
        from foundations.global_state import log_manager
        return log_manager.get_logger(__name__)