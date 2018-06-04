class LocalFileSystemCacheBackend(object):

    def __init__(self, path):
        self._path = path

    def get(self, key):
        import dill as pickle
        import os.path

        if os.path.isfile(self._file_path(key)):
            with open(self._file_path(key), 'rb') as file:
                return pickle.load(file)
        else:
            return None

    def set(self, key, value):
        import dill as pickle

        with open(self._file_path(key), 'w+b') as file:
            return pickle.dump(value, file, protocol=2)

    def _file_path(self, key):
        return self._path + '/' + key
