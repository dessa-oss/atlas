class LocalPipelineArchive(object):

    class Tempfile(object):

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

    def __init__(self, name):
        import tarfile
        self._name = name
        self._tar = tarfile.open(self.archive(), "w:gz")

    def __enter__(self):
        self._tar.__enter__()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        return self._tar.__exit__(exception_type, exception_value, traceback)

    def append(self, name, item):
        import dill as pickle

        with self.Tempfile('w+b') as tempfile:
            pickle.dump(item, tempfile.file)
            tempfile.file.flush()
            self._tar.add(tempfile.path, arcname=name + '.pkl')

    def append_file(self, prefix, file_path):
        from os.path import basename
        name = basename(file_path)
        self._tar.add(file_path, arcname=prefix + '/' + name)

    def archive_name(self):
        return self._name + ".tgz"

    def archive(self):
        return self.archive_name()
