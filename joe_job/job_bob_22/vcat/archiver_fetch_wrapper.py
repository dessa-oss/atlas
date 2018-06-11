class ArchiverFetchWrapper(object):

    def __init__(self, archive_listing, stage_log_archive, persisted_data_archive, provenance_archive, job_source_archive, artifact_archive, miscellaneous_archive):
        self._archive_listing = archive_listing
        self._stage_log_archive = stage_log_archive
        self._persisted_data_archive = persisted_data_archive
        self._provenance_archive = provenance_archive
        self._job_source_archive = job_source_archive
        self._artifact_archive = artifact_archive
        self._miscellaneous_archive = miscellaneous_archive

    def __enter__(self):
        from vcat.pipeline_archiver_fetch import PipelineArchiverFetch
        return PipelineArchiverFetch(
            self._archive_listing,
            self._stage_log_archive,
            self._persisted_data_archive,
            self._provenance_archive,
            self._job_source_archive,
            self._artifact_archive,
            self._miscellaneous_archive
        )

    def __exit__(self, exception_type, exception_value, traceback):
        self._stage_log_archive.__exit__(
            exception_type, exception_value, traceback)
        self._persisted_data_archive.__exit__(
            exception_type, exception_value, traceback)
        self._provenance_archive.__exit__(
            exception_type, exception_value, traceback)
        self._job_source_archive.__exit__(
            exception_type, exception_value, traceback)
        self._artifact_archive.__exit__(
            exception_type, exception_value, traceback)
        self._miscellaneous_archive.__exit__(
            exception_type, exception_value, traceback)
