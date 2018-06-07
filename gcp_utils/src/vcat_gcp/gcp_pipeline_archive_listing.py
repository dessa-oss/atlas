class GCPPipelineArchiveListing(object):

    def __init__(self, bucket):
        from vcat_gcp.gcp_bucket import GCPBucket

        self._gcp_bucket = GCPBucket(bucket)

    def track_pipeline(self, pipeline_name):
        self._gcp_bucket.upload_from_string('pipeline_archives/' + pipeline_name + '.tracker', pipeline_name)

    def get_pipeline_names(self):
        file_paths = self._gcp_bucket.list_files('pipeline_archives/*.tracker')

        return [self._gcp_bucket.download_as_string(path) for path in file_paths]
