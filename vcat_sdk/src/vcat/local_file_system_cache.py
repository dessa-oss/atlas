class LocalFileSystemCache(object):

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
            return pickle.dump(value, file)
        return value

    def get_or_set(self, key, value):
      return self.get(key) or self.set(key, value)

    def get_or_set_callback(self, key, callback):
      return self.get(key) or self.set(key, callback())

    def _file_path(self, key):
        return self._path + '/' + key
