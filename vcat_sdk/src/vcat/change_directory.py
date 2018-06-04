class ChangeDirectory(object):

    @staticmethod
    def from_file_path(path):
        from os.path import dirname

        directory = dirname(path)
        return ChangeDirectory(directory)

    def __init__(self, path):
        self._path = path
        self._current_directory = None

    def __enter__(self):
        from os import chdir
        from os import getcwd

        self._current_directory = getcwd()
        chdir(self._path)

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        from os import chdir

        chdir(self._current_directory)
