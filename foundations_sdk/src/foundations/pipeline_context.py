"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.provenance import Provenance
from foundations.stage_context import StageContext
from foundations.thread_manager import ThreadManager

class PipelineContext(object):

    def __init__(self):
        import uuid

        self.file_name = str(uuid.uuid4()) + ".json"
        self.provenance = Provenance()
        self.stage_contexts = {}
        self.global_stage_context = StageContext()
        self.global_stage_context.uuid = 'global'
        self._stage_log_archive_loaded = False
        self._persisted_data_archive_loaded = False
        self._provenance_archive_loaded = False
        self._job_source_archive_loaded = False
        self._artifact_archive_loaded = False
        self._miscellaneous_archive_loaded = False

    def mark_fully_loaded(self):
        self._stage_log_archive_loaded = True
        self._persisted_data_archive_loaded = True
        self._provenance_archive_loaded = True
        self._job_source_archive_loaded = True
        self._artifact_archive_loaded = True
        self._miscellaneous_archive_loaded = True

    def add_stage_context(self, stage_context):
        self.stage_contexts[stage_context.uuid] = stage_context

    def fill_provenance(self, config_manager):
        self.provenance.fill_all(config_manager)

    def save(self, result_saver):
        result_saver.save(self.file_name, self._context())

    def save_to_archive(self, archiver):
        from foundations.unserializable_placeholder import UnserializablePlaceholder

        archiver.append_tracker()
        archiver.append_miscellaneous('stage_listing', self._stage_keys())
        self.global_stage_context.save_to_archive(archiver)

        for stage_context in self.stage_contexts.values():
            stage_context.save_all_but_persisted_data(archiver)

            try:
                stage_context.save_persisted_data(archiver)
            except TypeError:
                self._log_failed_data_persist(stage_context)

                stage_uuid = stage_context.uuid
                stage_name = self._lookup_stage_name_from_uuid(stage_uuid)
                job_name = self.file_name

                stage_context.stage_output = UnserializablePlaceholder(stage_name, stage_uuid, job_name)
                stage_context.save_persisted_data(archiver)

        self.provenance.save_to_archive(archiver)

    def _log_failed_data_persist(self, stage_context):
        from foundations import log_manager
        logger = log_manager.get_logger(__name__)

        format_string = "Cannot persist value of type '{}' from stage '{}': {}"

        stage_type = type(stage_context.stage_output).__name__
        stage_name = self._lookup_stage_name_from_uuid(stage_context.uuid)
        stage_value = stage_context.stage_output

        warning_message = format_string.format(stage_type, stage_name, stage_value)
        logger.warning(warning_message)
    
    def _lookup_stage_name_from_uuid(self, uuid):
        stage_hierarchy = self.provenance.stage_hierarchy
        stage_hierarchy_entries = stage_hierarchy.entries
        return stage_hierarchy_entries[uuid].function_name

    def _stage_keys(self):
        return list(self.stage_contexts.keys())

    def load_stage_log_from_archive(self, archiver):
        self.load_miscellaneous_from_archive(archiver)
        if not self._stage_log_archive_loaded:
            self._stage_log_archive_loaded = True

            self.provenance.load_stage_log_from_archive(archiver)
            self.global_stage_context.load_stage_log_from_archive(archiver)

            for stage_context in self.stage_contexts.values():
                stage_context.load_stage_log_from_archive(archiver)

    def load_persisted_data_from_archive(self, archiver):
        self.load_miscellaneous_from_archive(archiver)
        if not self._persisted_data_archive_loaded:
            self._persisted_data_archive_loaded = True

            self.provenance.load_persisted_data_from_archive(archiver)
            self.global_stage_context.load_persisted_data_from_archive(archiver)

            for stage_context in self.stage_contexts.values():
                stage_context.load_persisted_data_from_archive(archiver)

    def load_provenance_from_archive(self, archiver):
        if not self._provenance_archive_loaded:
            self.load_miscellaneous_from_archive(archiver)
            self._provenance_archive_loaded = True

            self.provenance.load_provenance_from_archive(archiver)
            self.global_stage_context.load_provenance_from_archive(archiver)

            for stage_context in self.stage_contexts.values():
                stage_context.load_provenance_from_archive(archiver)

    def load_job_source_from_archive(self, archiver):
        if not self._job_source_archive_loaded:
            self._job_source_archive_loaded = True

            self.provenance.load_job_source_from_archive(archiver)
            self.global_stage_context.load_job_source_from_archive(archiver)

            for stage_context in self.stage_contexts.values():
                stage_context.load_job_source_from_archive(archiver)

    def load_artifact_from_archive(self, archiver):
        if not self._artifact_archive_loaded:
            self._artifact_archive_loaded = True

            self.provenance.load_artifact_from_archive(archiver)
            self.global_stage_context.load_artifact_from_archive(archiver)

            for stage_context in self.stage_contexts.values():
                stage_context.load_artifact_from_archive(archiver)

    def load_miscellaneous_from_archive(self, archiver):
        if not self._miscellaneous_archive_loaded:
            self._miscellaneous_archive_loaded = True

            stage_uuids = archiver.fetch_miscellaneous('stage_listing') or []

            def _create_stage_contexts(stage_uuid):
                stage_context = StageContext()
                stage_context.uuid = stage_uuid
                return stage_context

            stage_contexts = list(map(_create_stage_contexts, stage_uuids))

            self.provenance.load_miscellaneous_from_archive(archiver)
            self.global_stage_context.load_miscellaneous_from_archive(archiver)

            for stage_context in stage_contexts:
                stage_context.load_miscellaneous_from_archive(archiver)
                    
            for stage_context in stage_contexts:        
                self.add_stage_context(stage_context)

    def load_from_archive(self, archiver):
        self.load_stage_log_from_archive(archiver)
        self.load_persisted_data_from_archive(archiver)
        self.load_provenance_from_archive(archiver)
        self.load_job_source_from_archive(archiver)
        self.load_artifact_from_archive(archiver)
        self.load_miscellaneous_from_archive(archiver)

    def _context(self):
        stringified_stage_contexts = {}

        for uuid, context in self.stage_contexts.items():
            stringified_stage_contexts[uuid] = context._context()

        return {
            "provenance": self.provenance,
            "stage_contexts": stringified_stage_contexts,
            "global_stage_context": self.global_stage_context._context()
        }
