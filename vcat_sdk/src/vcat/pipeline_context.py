from vcat.provenance import Provenance
from vcat.stage_context import StageContext

class PipelineContext(object):

    def __init__(self):
        import uuid

        self.predictions = {}
        self.provenance = Provenance()
        self.file_name = str(uuid.uuid4()) + ".json"
        self.stage_contexts = {}

        self.global_stage_context = StageContext()

    def add_stage_context(self, stage_context):
        self.stage_contexts[stage_context.uuid] = stage_context

    def fill_provenance(self):
        self.provenance.fill_all()

    def save(self, result_saver):
        result_saver.save(self.file_name, self._context())

    def _context(self):
        stringified_stage_contexts = {}

        for uuid, context in self.stage_contexts.iteritems():
            stringified_stage_contexts[uuid] = context._context()

        return {
            "provenance": self.provenance,
            "stage_contexts": stringified_stage_contexts,
            "global_stage_context": self.global_stage_context._context()
        }
