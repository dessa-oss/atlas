from vcat.provenance import Provenance
from vcat.stage_context import StageContext

class PipelineContext(object):

    def __init__(self):
        import uuid

        self.file_name = str(uuid.uuid4()) + ".json"
        self.provenance = Provenance()
        self.stage_contexts = {}
        
        self.global_stage_context = StageContext()
        self.global_stage_context.uuid = 'global'

    def add_stage_context(self, stage_context):
        self.stage_contexts[stage_context.uuid] = stage_context

    def fill_provenance(self):
        self.provenance.fill_all()

    def save(self, result_saver):
        result_saver.save(self.file_name, self._context())

    def save_to_archive(self, archiver):
        archiver.append_tracker()
        archiver.append_miscellanous('stages', self.stage_contexts.keys())
        self.global_stage_context.save_to_archive(archiver)
        for stage_context in self.stage_contexts.values():
            stage_context.save_to_archive(archiver)
        self.provenance.save_to_archive(archiver)

    def load_from_archive(self, archiver):
        stage_uuids = archiver.fetch_miscellanous('stages')
        self.global_stage_context.load_from_archive(archiver)
        for stage_uuid in stage_uuids:
            stage_context = StageContext()
            stage_context.uuid = stage_uuid
            stage_context.load_from_archive(archiver)
        self.provenance.load_from_archive(archiver)

    def _context(self):
        stringified_stage_contexts = {}

        for uuid, context in self.stage_contexts.iteritems():
            stringified_stage_contexts[uuid] = context._context()

        return {
            "provenance": self.provenance,
            "stage_contexts": stringified_stage_contexts,
            "global_stage_context": self.global_stage_context._context()
        }
