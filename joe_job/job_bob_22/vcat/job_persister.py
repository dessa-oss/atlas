from vcat.archiver_fetch_wrapper import ArchiverFetchWrapper


class JobPersister(object):

    def __init__(self, job):
        self._pipeline_context = job.pipeline_context()

    def persist(self):
        from vcat.pipeline_archiver import PipelineArchiver

        archive_listing = JobPersister._load_archive_listing('archive_listing')
        with JobPersister._load_archive('stage_log_archive') as stage_log_archive, \
                JobPersister._load_archive('persisted_data_archive') as persisted_data_archive, \
                JobPersister._load_archive('provenance_archive') as provenance_archive, \
                JobPersister._load_archive('job_source_archive') as job_source_archive, \
                JobPersister._load_archive('artifact_archive') as artifact_archive, \
                JobPersister._load_archive('miscellaneous_archive') as miscellaneous_archive:

            archiver = PipelineArchiver(self._pipeline_context.file_name,
                                        archive_listing,
                                        stage_log_archive,
                                        persisted_data_archive,
                                        provenance_archive,
                                        job_source_archive,
                                        artifact_archive,
                                        miscellaneous_archive)
            self._pipeline_context.save_to_archive(archiver)

    @staticmethod
    def load_archiver_fetch():
        return ArchiverFetchWrapper(
            JobPersister._load_archive_listing('archive_listing'),
            JobPersister._load_archive('stage_log_archive'),
            JobPersister._load_archive('persisted_data_archive'),
            JobPersister._load_archive('provenance_archive'),
            JobPersister._load_archive('job_source_archive'),
            JobPersister._load_archive('artifact_archive'),
            JobPersister._load_archive('miscellaneous_archive')
        )

    @staticmethod
    def _load_archive(name):
        from vcat.global_state import config_manager
        from vcat.null_archive import NullArchive

        return config_manager.reflect_instance(name, 'archive', lambda: NullArchive())

    @staticmethod
    def _load_archive_listing(name):
        from vcat.global_state import config_manager
        from vcat.null_pipeline_archive_listing import NullArchiveListing

        return config_manager.reflect_instance(name, 'archive_listing', lambda: NullArchiveListing())
