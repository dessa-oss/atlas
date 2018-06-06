class SimpleTempfile(object):

    def __init__(self, mode):
        self.path = None
        self.file = None
        self._mode = mode

    def __enter__(self):
        import tempfile
        import os

        file_descriptor, self.path = tempfile.mkstemp()
        self.file = os.fdopen(file_descriptor, self._mode)
        self.file.__enter__()

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        import os

        try:
            self.file.__exit__()
        finally:
            os.remove(self.path)

