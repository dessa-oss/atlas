class JobPersister(object):

    def __init__(self, job):
        self._pipeline_context = job.pipeline_context()

    def persist(self):
        from vcat.pipeline_archiver import PipelineArchiver

        archive_listing = self._load_archive_listing('archive_listing')
        with self._load_archive('stage_log_archive') as stage_log_archive, \
            self._load_archive('persisted_data_archive') as persisted_data_archive, \
            self._load_archive('provenance_archive') as provenance_archive, \
            self._load_archive('job_source_archive') as job_source_archive, \
            self._load_archive('artifact_archive') as artifact_archive, \
            self._load_archive('miscellaneous_archive') as miscellaneous_archive:

            archiver = PipelineArchiver(self._pipeline_context.file_name, 
                archive_listing, 
                stage_log_archive, 
                persisted_data_archive, 
                provenance_archive, 
                job_source_archive, 
                artifact_archive, 
                miscellaneous_archive)
            self._pipeline_context.save_to_archive(archiver)

    def _load_archive(self, name):
        from vcat.global_state import config_manager
        from vcat.null_archive import NullArchive

        return config_manager.reflect_instance(name, 'archive', lambda: NullArchive())

    def _load_archive_listing(self, name):
        from vcat.global_state import config_manager
        from vcat.null_pipeline_archive_listing import NullArchiveListing

        return config_manager.reflect_instance(name, 'archive_listing', lambda: NullArchiveListing())
