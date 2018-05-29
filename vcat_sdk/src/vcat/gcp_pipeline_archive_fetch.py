class GCPPipelineArchiveFetch(object):

    def __init__(self):
        from google.cloud.storage import Client
        from googleapiclient import discovery

        self._gcp_bucket_connection = Client()
        self._result_bucket_connection = self._gcp_bucket_connection.get_bucket(
            'tango-result-test')

    def fetch_results(self):
        objects = self._result_bucket_connection.list_blobs(
            prefix='pipeline_archives/', delimiter='/')
        return objects