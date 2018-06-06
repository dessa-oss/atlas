from vcat.utils import file_archive_name
from vcat.utils import file_archive_name_with_additional_prefix
from vcat.local_file_system_bucket import LocalFileSystemBucket


class LocalFileSystemPipelineArchive(object):

    def __init__(self, path=None):
        from os import getcwd
        from os.path import abspath

        bucket_path = path or getcwd()
        bucket_path = abspath(bucket_path)
        self._bucket = LocalFileSystemBucket(bucket_path)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def append(self, name, item, prefix=None):
        import dill as pickle

        serialized_item = pickle.dumps(item)
        self.append_binary(name, serialized_item, prefix)

    def append_binary(self, name, serialized_item, prefix=None):
        arcname = file_archive_name(prefix, name)
        self._bucket.upload_from_string(arcname, serialized_item)

    def append_file(self, file_prefix, file_path, prefix=None, target_name=None):
        from os.path import basename

        name = target_name or basename(file_path)
        arcname = file_archive_name_with_additional_prefix(
            prefix, file_prefix, name)
        with open(file_path) as file:
            self._bucket.upload_from_file(arcname, file)

    def fetch(self, name, prefix=None):
        import dill as pickle

        serialized_item = self.fetch_binary(name, prefix)
        if serialized_item is None:
            return None
        else:
            return pickle.loads(serialized_item)

    def fetch_binary(self, name, prefix=None):
        arcname = file_archive_name(prefix, name)
        if self._bucket.exists(arcname):
            return self._bucket.download_as_string(arcname)
        else:
            return None

    def fetch_to_file(self, file_prefix, file_path, prefix=None, target_name=None):
        from os.path import basename
        name = target_name or basename(file_path)
        arcname = file_archive_name_with_additional_prefix(
            prefix, file_prefix, name)
        if self._bucket.exists(arcname):
            with open(file_path, 'w+b') as file:
                self._bucket.download_to_file(arcname, file)
