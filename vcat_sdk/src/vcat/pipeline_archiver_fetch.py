from pipeline_archiver import PipelineArchiver


class PipelineArchiverFetch(object):

    def __init__(self, archive_listing, stage_log_archive, persisted_data_archive, provenance_archive, job_source_archive, artifact_archive, miscellaneous_archive):
        self._archive_listing = archive_listing
        self._stage_log_archive = stage_log_archive
        self._persisted_data_archive = persisted_data_archive
        self._provenance_archive = provenance_archive
        self._job_source_archive = job_source_archive
        self._artifact_archive = artifact_archive
        self._miscellaneous_archive = miscellaneous_archive

    def fetch_archivers(self):
        job_names = self._archive_listing.get_pipeline_names()
        return [PipelineArchiver(name, self._archive_listing, self._stage_log_archive, self._persisted_data_archive, self._provenance_archive, self._job_source_archive, self._artifact_archive, self._miscellaneous_archive) for name in job_names]
