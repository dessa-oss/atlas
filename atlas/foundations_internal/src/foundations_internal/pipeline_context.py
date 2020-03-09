
from foundations_internal.provenance import Provenance


class PipelineContext(object):

    def __init__(self):
        self._file_name = None
        self.provenance = Provenance()
        self._persisted_data_archive_loaded = False
        self._provenance_archive_loaded = False
        self._job_source_archive_loaded = False
        self._artifact_archive_loaded = False

    @property
    def file_name(self):
        if not self._file_name:
            raise ValueError('Job ID is currently undefined, please set before retrieving')
        return self._file_name
    
    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @property
    def job_id(self):
        return self.file_name

    def mark_fully_loaded(self):
        self._persisted_data_archive_loaded = True
        self._provenance_archive_loaded = True
        self._job_source_archive_loaded = True
        self._artifact_archive_loaded = True

    def fill_provenance(self, config_manager):
        self.provenance.fill_all(config_manager)

    def save(self, result_saver):
        result_saver.save(self.file_name, self._context())

    def save_to_archive(self, archiver):
        archiver.append_tracker()
        self.provenance.save_to_archive(archiver)

    def load_persisted_data_from_archive(self, archiver):
        if not self._persisted_data_archive_loaded:
            self._persisted_data_archive_loaded = True

            self.provenance.load_persisted_data_from_archive(archiver)

    def load_provenance_from_archive(self, archiver):
        if not self._provenance_archive_loaded:
            self._provenance_archive_loaded = True

            self.provenance.load_provenance_from_archive(archiver)

    def load_job_source_from_archive(self, archiver):
        if not self._job_source_archive_loaded:
            self._job_source_archive_loaded = True

            self.provenance.load_job_source_from_archive(archiver)

    def load_artifact_from_archive(self, archiver):
        if not self._artifact_archive_loaded:
            self._artifact_archive_loaded = True

            self.provenance.load_artifact_from_archive(archiver)

    def load_from_archive(self, archiver):
        self.load_persisted_data_from_archive(archiver)
        self.load_provenance_from_archive(archiver)
        self.load_job_source_from_archive(archiver)
        self.load_artifact_from_archive(archiver)

    def _context(self):
        stringified_stage_contexts = {}

        return {
            "provenance": self.provenance,
            "stage_contexts": stringified_stage_contexts,
        }
