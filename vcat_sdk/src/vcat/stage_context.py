class StageContext(object):
    def __init__(self):
        self._stage_log = {}
        self._meta_data = {}
        self._data_uuid = None
        self._stage_output = None
        self._uuid = None
        self._error_information = None
        self._model_data = None
        self._start_time = None
        self._end_time = None
        self._delta_time = None

    def add_error_information(self, exception_info):
        import traceback
        self._error_information = {
            "type": exception_info[0],
            "exception": exception_info[1],
            "traceback": traceback.extract_tb(exception_info[2])
        }

    def save_model(model):
        self._model_data = model

    def _context(self):
        return {
            "uuid": self._uuid,
            "stage_log": self._stage_log,
            "meta_data": self._meta_data,
            "data_uuid": self._data_uuid,
            "stage_output": self._stage_output,
            "error_information": self._error_information,
            "start_time": self._start_time,
            "end_time": self._end_time,
            "delta_time": self._delta_time
        }