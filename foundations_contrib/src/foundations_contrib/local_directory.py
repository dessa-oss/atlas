"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.change_directory import ChangeDirectory


class LocalDirectory(object):

    class File(object):

        def __init__(self, path):
            self._file = None
            self._path = path

        def open(self, mode):
            return open(self._path, mode)

    def __init__(self):
        from os import getcwd
        self._path = getcwd()

    def get_files(self, pathname):
        from glob import glob

        with ChangeDirectory(self._path):
            for file_path in glob(pathname):
                yield self.File(file_path)
