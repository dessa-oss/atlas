"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class WorkingDirectoryStack(object):

    def __init__(self):
        self._stack = []

    def __enter__(self):
        from os import getcwd

        directory = getcwd()
        self._stack.append(directory)

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        from os import chdir

        directory = self._stack.pop()
        chdir(directory)
