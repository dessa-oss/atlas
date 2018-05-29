from vcat.provenance import Provenance


class PipelineContext(object):

    def __init__(self):
        import uuid

        self.results = {}
        self.config = {}
        self.predictions = {}
        self.provenance = Provenance()
        self.meta_data = {}
        self.persisted_data = {}
        self.error = None
        self.pipeline_errors = {}
        self.file_name = str(uuid.uuid4()) + ".json"

    def fill_provenance(self):
        self.provenance.fill_all()

    def save(self, result_saver):
        result_saver.save(self.file_name, self._context())

    def nice_error(self, exception_info):
        import traceback
        return {
            "type": exception_info[0],
            "exception": exception_info[1],
            "traceback": traceback.extract_tb(exception_info[2])
        }

    def _context(self):
        return {
            "results": self.results,
            "config": self.config,
            "provenance": self.provenance,
            "meta_data": self.meta_data,
            "persisted_data": self.persisted_data,
            "error": self.error,
            "pipeline_errors": self.pipeline_errors,
        }
