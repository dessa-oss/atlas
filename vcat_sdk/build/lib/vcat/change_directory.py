"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.working_directory_stack import WorkingDirectoryStack


class ChangeDirectory(object):

    @staticmethod
    def from_file_path(path):
        from os.path import dirname

        directory = dirname(path)
        return ChangeDirectory(directory)

    def __init__(self, path):
        self._path = path
        self._stack = WorkingDirectoryStack()

    def __enter__(self):
        from os import chdir

        self._stack.__enter__()
        chdir(self._path)

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._stack.__exit__(exception_type, exception_value, traceback)
