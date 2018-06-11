"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class StageContext(object):

    def __init__(self):
        self.stage_log = {}
        self.meta_data = {}
        self.data_uuid = None
        self.stage_output = None
        self.uuid = None
        self.error_information = None
        self.model_data = None
        self.start_time = None
        self.end_time = None
        self.delta_time = None
        self.is_context_aware = False
        self.used_cache = False
        self.cache_uuid = None
        self.cache_read_time = False
        self.cache_write_time = None
        self.has_stage_output = None

    def set_stage_output(self, stage_output):
        self.stage_output = stage_output
        self.has_stage_output = True

    def add_error_information(self, exception_info):
        import traceback
        self._error_information = {
            "type": exception_info[0],
            "exception": exception_info[1],
            "traceback": traceback.extract_tb(exception_info[2])
        }

    def save_to_archive(self, archiver):
        archiver.append_stage_log(self.uuid, self.stage_log)
        archiver.append_stage_persisted_data(self.uuid, self.stage_output)
        archiver.append_stage_model_data(self.uuid, self.model_data)
        archiver.append_stage_miscellaneous(
            self.uuid, 'stage_context', self._archive_stage_context())

    def load_stage_log_from_archive(self, archiver):
        self.stage_log = archiver.fetch_stage_log(self.uuid)

    def load_persisted_data_from_archive(self, archiver):
        self.stage_output = archiver.fetch_stage_persisted_data(self.uuid)
        self.model_data = archiver.fetch_stage_model_data(self.uuid)

    def load_provenance_from_archive(self, archiver):
        pass

    def load_job_source_from_archive(self, archiver):
        pass

    def load_artifact_from_archive(self, archiver):
        pass

    def load_miscellaneous_from_archive(self, archiver):
        archive_stage_context = archiver.fetch_stage_miscellaneous(
            self.uuid, 'stage_context') or {}
        self._load_archive_stage_context(archive_stage_context)

    def time_callback(self, callback):
        import time

        start_time = time.time()
        return_value = callback()
        end_time = time.time()

        self.start_time = start_time
        self.end_time = end_time
        self.delta_time = end_time - start_time

        return return_value

    def _load_archive_stage_context(self, archive_stage_context):
        self.meta_data = archive_stage_context.get('meta_data', self.meta_data)
        self.data_uuid = archive_stage_context.get('data_uuid', self.data_uuid)
        self.uuid = archive_stage_context.get('uuid', self.uuid)
        self.error_information = archive_stage_context.get(
            'error_information', self.error_information)
        self.start_time = archive_stage_context.get(
            'start_time', self.start_time)
        self.end_time = archive_stage_context.get('end_time', self.end_time)
        self.delta_time = archive_stage_context.get(
            'delta_time', self.delta_time)
        self.is_context_aware = archive_stage_context.get(
            'is_context_aware', self.is_context_aware)
        self.used_cache = archive_stage_context.get(
            'used_cache', self.used_cache)
        self.cache_uuid = archive_stage_context.get(
            'cache_uuid', self.cache_uuid)
        self.cache_read_time = archive_stage_context.get(
            'cache_read_time', self.cache_read_time)
        self.cache_write_time = archive_stage_context.get(
            'cache_write_time', self.cache_write_time)
        self.has_stage_output = archive_stage_context.get(
            'has_stage_output', self.has_stage_output)

    def _archive_stage_context(self):
        return {
            'meta_data': self.meta_data,
            'data_uuid': self.data_uuid,
            'uuid': self.uuid,
            'error_information': self.error_information,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'delta_time': self.delta_time,
            'is_context_aware': self.is_context_aware,
            'used_cache': self.used_cache,
            'cache_uuid': self.cache_uuid,
            'cache_read_time': self.cache_read_time,
            'cache_write_time': self.cache_write_time,
            'has_stage_output': self.has_stage_output,
        }

    def _context(self):
        return {
            "uuid": self.uuid,
            "stage_log": self.stage_log,
            "meta_data": self.meta_data,
            "data_uuid": self.data_uuid,
            "stage_output": self.stage_output,
            "error_information": self.error_information,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "delta_time": self.delta_time,
            "is_context_aware": self.is_context_aware,
            "used_cache": self.used_cache,
            "cache_uuid": self.cache_uuid,
            "cache_read_time": self.cache_read_time,
            "cache_write_time": self.cache_write_time,
            "has_stage_output": self.has_stage_output,
        }
