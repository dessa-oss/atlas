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

    def load_from_archive(self, archiver):
        self.stage_log = archiver.fetch_stage_log(self.uuid)
        self.stage_output = archiver.fetch_stage_persisted_data(self.uuid)
        self.model_data = archiver.fetch_stage_model_data(self.uuid)
        archive_stage_context = archiver.fetch_stage_miscellaneous(
            self.uuid, 'stage_context')
        self._load_archive_stage_context(archive_stage_context)

    def _load_archive_stage_context(self, archive_stage_context):
        self.meta_data = archive_stage_context['meta_data']
        self.data_uuid = archive_stage_context['data_uuid']
        self.uuid = archive_stage_context['uuid']
        self.error_information = archive_stage_context['error_information']
        self.start_time = archive_stage_context['start_time']
        self.end_time = archive_stage_context['end_time']
        self.delta_time = archive_stage_context['delta_time']
        self.is_context_aware = archive_stage_context['is_context_aware']

    def time_callback(self, callback):
        import time

        start_time = time.time()
        return_value = callback()
        end_time = time.time()
        
        self.start_time = start_time
        self.end_time = end_time
        self.delta_time = end_time - start_time

        return return_value

    def _archive_stage_context(self):
        return {
            'meta_data': self.meta_data,
            'data_uuid': self.data_uuid,
            'uuid': self.uuid,
            'error_information': self.error_information,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'delta_time': self.delta_time,
            'is_context_aware': self.is_context_aware
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
            "is_context_aware": self.is_context_aware
        }
