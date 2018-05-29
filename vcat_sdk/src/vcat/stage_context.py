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

    def load_from_archive(self, archiver):
        self.stage_log = archiver.fetch_stage_log(self.uuid)
        self.stage_output = archiver.fetch_stage_persisted_data(self.uuid)

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
