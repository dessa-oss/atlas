from pipeline_archiver import PipelineArchiver


class GCPPipelineArchiveFetch(object):

    def __init__(self, stage_log_archive, persisted_data_archive, provenance_archive, job_source_archive, artifact_archive, miscellanous_archive):
        from google.cloud.storage import Client
        from googleapiclient import discovery

        self._gcp_bucket_connection = Client()
        self._result_bucket_connection = self._gcp_bucket_connection.get_bucket(
            'tango-result-test')

        self._stage_log_archive = stage_log_archive
        self._persisted_data_archive = persisted_data_archive
        self._provenance_archive = provenance_archive
        self._job_source_archive = job_source_archive
        self._artifact_archive = artifact_archive
        self._miscellanous_archive = miscellanous_archive

    def fetch_archivers(self):
        from os.path import basename
        from os.path import splitext

        objects = self._result_bucket_connection.list_blobs(
            prefix='pipeline_archives/', delimiter='/')

        job_names = [bucket_object.download_as_string()
                     for bucket_object in objects]
        return [PipelineArchiver(name, self._stage_log_archive, self._persisted_data_archive, self._provenance_archive, self._job_source_archive, self._artifact_archive, self._miscellanous_archive) for name in job_names]
