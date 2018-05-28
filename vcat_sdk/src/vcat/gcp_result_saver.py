class GCPResultSaver(object):

    def __init__(self):
        from google.cloud.storage import Client
        from googleapiclient import discovery

        self._gcp_bucket_connection = Client()
        self._result_bucket_connection = self._gcp_bucket_connection.get_bucket(
            'tango-result-test')

    def save(self, name, results):
        import dill as pickle

        result_object = self._result_bucket_connection.blob(
            "contexts/" + name + ".pkl")
        serialized_results = pickle.dumps(results)
        result_object.upload_from_string(serialized_results)

    def clear(self):
        raise NotImplementedError()
