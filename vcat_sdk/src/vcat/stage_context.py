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

    def add_error_information(self, exception_info):
        import traceback
        self._error_information = {
            "type": exception_info[0],
            "exception": exception_info[1],
            "traceback": traceback.extract_tb(exception_info[2])
        }

    def save_model(self, model):
        self._model_data = model

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
            "delta_time": self.delta_time
        }
