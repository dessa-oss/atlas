"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class SimpleTempfile(object):

    def __init__(self, mode, suffix=None):
        self.path = None
        self.file = None
        self.name = None
        self._suffix = suffix
        self._mode = mode

    def seek(self, *args, **kwargs):
        return self.file.seek(*args, **kwargs)

    def write(self, *args, **kwargs):
        return self.file.write(*args, **kwargs)

    def read(self, *args, **kwargs):
        return self.file.read(*args, **kwargs)

    def flush(self, *args, **kwargs):
        return self.file.flush(*args, **kwargs)

    def write_and_flush(self, data):
        self.write(data)
        self.flush()

    def __enter__(self):
        import tempfile
        import os

        file_descriptor, self.path = tempfile.mkstemp(suffix=self._suffix)
        self.file = os.fdopen(file_descriptor, self._mode)
        self.file.__enter__()
        self.name = self.path

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        import os

        try:
            self.name = None
            self.file.__exit__()
            self.file = None
        finally:
            os.remove(self.path)
