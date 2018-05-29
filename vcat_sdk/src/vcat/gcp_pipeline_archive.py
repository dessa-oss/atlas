class GCPPipelineArchive(object):

    def __init__(self, job_name):
        from google.cloud.storage import Client
        from googleapiclient import discovery

        self._gcp_bucket_connection = Client()
        self._result_bucket_connection = self._gcp_bucket_connection.get_bucket(
            'tango-result-test')
        self._job_name = job_name

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def append(self, name, item):
        import dill as pickle

        serialized_item = pickle.dumps(item)
        bucket_object = self._bucket_object(name)
        bucket_object.upload_from_string(serialized_item)

    def append_file(self, prefix, file_path):
        from os.path import basename
        name = basename(file_path)
        bucket_object = self._bucket_object(prefix + '/' + name)
        with open(file_path, 'rb') as file:
            bucket_object.upload_from_file(file)

    def fetch(self, name):
        import dill as pickle

        bucket_object = self._bucket_object(name)
        if bucket_object.exists():
            serialized_item = bucket_object.download_as_string()
            return pickle.loads(serialized_item)
        else:
            return None

    def fetch_to_file(self, prefix, file_path):
        from os.path import basename
        name = basename(file_path)
        bucket_object = self._bucket_object(prefix + '/' + name)
        if bucket_object.exists():
            with open(file_path, 'w+b') as file:
                bucket_object.download_to_file(file)

    def _bucket_object(self, name):
        return self._result_bucket_connection.blob('pipeline_archives/' + self._job_name + '/' + name)
