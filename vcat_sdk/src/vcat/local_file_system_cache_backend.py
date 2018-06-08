class LocalFileSystemCacheBackend(object):

    def __init__(self, path):
        from vcat.local_file_system_bucket import LocalFileSystemBucket

        self._bucket = LocalFileSystemBucket(path)

    def get(self, key):
        from vcat.simple_tempfile import SimpleTempfile
        import dill as pickle

        if self._bucket.exists(key):
            with SimpleTempfile('rw+b') as temp_file:
                self._bucket.download_to_file(key, temp_file.file)
                return pickle.load(temp_file.file)
        else:
            return None

    def set(self, key, value):
        import dill as pickle
        from vcat.simple_tempfile import SimpleTempfile

        with SimpleTempfile('rw+b') as temp_file:
            pickle.dump(value, temp_file.file)
            temp_file.flush()
            temp_file.seek(0)
            self._bucket.upload_from_file(key, temp_file.file)
