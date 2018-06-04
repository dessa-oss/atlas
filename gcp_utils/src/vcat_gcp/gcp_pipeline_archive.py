from vcat.utils import file_archive_name
from vcat.utils import file_archive_name_with_additional_prefix


class GCPPipelineArchive(object):

    def __init__(self):
        from google.cloud.storage import Client
        from googleapiclient import discovery

        self._gcp_bucket_connection = Client()
        self._result_bucket_connection = self._gcp_bucket_connection.get_bucket(
            'tango-result-test')

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def append(self, name, item, prefix=None):
        import dill as pickle

        serialized_item = pickle.dumps(item, protocol=2)
        self.append_binary(name + '.pkl', serialized_item, prefix)

    def append_binary(self, name, serialized_item, prefix=None):
        arcname = file_archive_name(prefix, name)
        bucket_object = self._bucket_object(arcname)
        bucket_object.upload_from_string(serialized_item)

    def append_file(self, file_prefix, file_path, prefix=None, target_name=None):
        from os.path import basename
        name = target_name or basename(file_path)
        arcname = file_archive_name_with_additional_prefix(
            prefix, file_prefix, name)
        bucket_object = self._bucket_object(arcname)
        with open(file_path, 'rb') as file:
            bucket_object.upload_from_file(file)

    def fetch(self, name, prefix=None):
        import dill as pickle

        serialized_item = self.fetch_binary(name + '.pkl', prefix)
        if serialized_item is not None:
            return pickle.loads(serialized_item)
        else:
            return None

    def fetch_binary(self, name, prefix=None):
        import dill as pickle

        arcname = file_archive_name(prefix, name)
        bucket_object = self._bucket_object(arcname)
        if bucket_object.exists():
            return bucket_object.download_as_string()
        else:
            return None

    def fetch_to_file(self, file_prefix, file_path, prefix=None, target_name=None):
        from os.path import basename
        name = target_name or basename(file_path)
        arcname = file_archive_name_with_additional_prefix(
            prefix, file_prefix, name)
        bucket_object = self._bucket_object(arcname)
        if bucket_object.exists():
            with open(file_path, 'w+b') as file:
                bucket_object.download_to_file(file)

    def _bucket_object(self, name):
        return self._result_bucket_connection.blob('pipeline_archives/' + name)
