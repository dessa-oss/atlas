"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class LocalFileSystemBucket(object):

    def __init__(self, path):
        from os.path import abspath
        from os import getcwd

        self._path = abspath(path or getcwd())
        self._log().debug('Creating bucket at path {}'.format(self._path))

    def upload_from_string(self, name, data):
        from vcat.utils import byte_string

        path = self._full_path(name)
        self._log().debug('Uploading %s (%s) from string', name, path)

        self._ensure_path_exists(name)
        with open(path, 'w+b') as file:
            data_bytes = byte_string(data)
            file.write(data_bytes)

    def upload_from_file(self, name, input_file):
        from shutil import copyfileobj

        path = self._full_path(name)
        self._log().debug('Uploading %s (%s) from %s', name, path, input_file.name)

        self._ensure_path_exists(name)
        with open(path, 'w+b') as file:
            copyfileobj(input_file, file)

    def exists(self, name):
        from os.path import isfile

        path = self._full_path(name)
        self._log().debug('Checking if %s exists (%s)', name, path)

        return isfile(path)

    def download_as_string(self, name):
        from vcat.utils import byte_string

        path = self._full_path(name)
        self._log().debug('Downloading %s (%s)', name, path)

        with open(path, 'rb') as file:
            data_bytes = file.read()
            return byte_string(data_bytes)

    def download_to_file(self, name, output_file):
        from shutil import copyfileobj

        path = self._full_path(name)
        self._log().debug('Downloading %s (%s) to %s', name, path, output_file.name)

        with open(path, 'rb') as file:
            copyfileobj(file, output_file)
            output_file.flush()
            output_file.seek(0)

    def list_files(self, pathname):
        from glob import glob
        from os import getcwd

        self._log().debug('Getting listing with pathname %s', pathname)

        full_pathname = self._full_path(pathname)
        self._log().debug('Listing with expanded pathname is %s', full_pathname)
        full_paths = glob(full_pathname)
        return [self._remove_bucket_path_from_file(path) for path in full_paths]
    
    def move(self, source, destination):
        from shutil import move

        self._ensure_path_exists(destination)
        move(self._full_path(source), self._full_path(destination))

    def _remove_bucket_path_from_file(self, path):
        return path[len(self._path)+1:]

    def _full_path(self, name):
        from os.path import join
        return join(self._path, name)

    def _ensure_path_exists(self, name):
        from vcat.utils import ensure_path_exists
        ensure_path_exists(self._path, name)

    def _log(self):
        from vcat.global_state import log_manager
        return log_manager.get_logger(__name__)
