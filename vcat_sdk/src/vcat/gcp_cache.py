class GCPCache(object):

    def __init__(self):
        from google.cloud.storage import Client
        from googleapiclient import discovery

        self._gcp_bucket_connection = Client()
        self._result_bucket_connection = self._gcp_bucket_connection.get_bucket(
            'tango-result-test')

    def get(self, key):
        import dill as pickle

        bucket_object = self._bucket_object(key)
        if bucket_object.exists():
            return pickle.loads(bucket_object.download_as_string())

    def set(self, key, value):
        import dill as pickle

        serialized_value = pickle.dumps(value)
        bucket_object = self._bucket_object(key)
        bucket_object.upload_from_string(serialized_value)
        return value

    def get_or_set(self, key, value):
        return self.get(key) or self.set(key, value)

    def get_or_set_callback(self, key, callback):
        return self.get(key) or self.set(key, callback())

    def _bucket_object(self, key):
        return self._result_bucket_connection.blob('cache/' + key)
