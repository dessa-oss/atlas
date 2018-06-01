class GCPPipelineArchiveListing(object):

    def __init__(self):
        from google.cloud.storage import Client
        from googleapiclient import discovery

        self._gcp_bucket_connection = Client()
        self._result_bucket_connection = self._gcp_bucket_connection.get_bucket(
            'tango-result-test')

    def track_pipeline(self, pipeline_name):
        bucket_object = self._result_bucket_connection.blob('pipeline_archives/' + pipeline_name + '.tracker')
        bucket_object.upload_from_string(pipeline_name)

    def get_pipeline_names(self):
        objects = self._result_bucket_connection.list_blobs(
            prefix='pipeline_archives/', delimiter='/')

        return [bucket_object.download_as_string() for bucket_object in objects]
