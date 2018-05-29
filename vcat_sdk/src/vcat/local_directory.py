import os


class LocalDirectory(object):

    class File(object):

        def __init__(self, path):
            self._file = None
            self._path = path

        def open(self, mode):
            return open(self._path, mode)

    def __init__(self):
        self._path = os.getcwd()

    def get_files(self, pathname):
        from glob import glob

        cwd = os.getcwd()
        os.chdir(self._path)
        for file_path in glob(pathname):
            yield self.File(file_path)
        os.chdir(cwd)
