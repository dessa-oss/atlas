from vcat.provenance import Provenance


class PipelineContext(object):

    def __init__(self):
        import uuid

        self.config = {}
        self.predictions = {}
        self.provenance = Provenance()
        self.pipeline_error = None
        self.start_time = None
        self.end_time = None
        self.delta_time = None
        self.file_name = str(uuid.uuid4()) + ".json"
        self.stage_contexts = {}

    def add_stage_context(self, stage_context):
        self.stage_contexts[stage_context.uuid] = stage_context

    def fill_provenance(self):
        self.provenance.fill_all()

    def save(self, result_saver):
        result_saver.save(self.file_name, self._context())

    def add_error_information(self, exception_info):
        import traceback
        self.pipeline_error = {
            "type": exception_info[0],
            "exception": exception_info[1],
            "traceback": traceback.extract_tb(exception_info[2])
        }

    def _context(self):
        stringified_stage_contexts = {}

        for uuid, context in self.stage_contexts.iteritems():
            stringified_stage_contexts[uuid] = context._context()

        return {
            "config": self.config,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "delta_time": self.delta_time,
            "provenance": self.provenance,
            "pipeline_errors": self.pipeline_error,
            "stage_contexts": stringified_stage_contexts
        }
