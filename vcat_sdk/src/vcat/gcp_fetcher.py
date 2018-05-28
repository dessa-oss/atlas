class GCPFetcher(object):

    def __init__(self):
        from google.cloud.storage import Client
        from googleapiclient import discovery

        self._gcp_bucket_connection = Client()
        self._result_bucket_connection = self._gcp_bucket_connection.get_bucket(
            'tango-result-test')

    def fetch_results(self):
        import dill as pickle

        objects = self._result_bucket_connection.list_blobs(prefix="contexts/")
        results_serialized = [result_object.download_as_string()
                              for result_object in objects]
        return [pickle.loads(result_serialized) for result_serialized in results_serialized]
