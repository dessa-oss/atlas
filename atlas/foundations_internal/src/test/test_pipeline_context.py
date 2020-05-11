
from foundations_spec import *
from foundations_internal.pipeline_context import PipelineContext


class TestPipelineContext(Spec):
    class MockStageContext(object):
        def __init__(self):
            self.uuid = None

        def set_uuid(self, uuid):
            self.uuid = uuid

    class MockResultSaver(object):
        def __init__(self):
            self.file_name = None
            self.context = None

        def save(self, file_name, context):
            self.file_name = file_name
            self.context = context

    class MockArchive(object):
        def __init__(self):
            self.stage_keys = None
            self.archive_provenance = None
            self.uuid = None
            self.stage_repeats_log_archive = 0
            self.stage_repeats_persisted_data = 0

        def append_tracker(self):
            return None

        def append_provenance(self, archive_provenance):
            self.archive_provenance = archive_provenance

        def fetch_provenance(self):
            pass

    class MockProvenance(object):
        def __init__(self):
            self.archiver = None
            self.load_provenace_counter = 0
            self.load_job_source_counter = 0
            self.load_artifact_counter = 0

        def load_provenance_from_archive(self, archiver):
            self.archiver = archiver
            self.load_provenace_counter += 1

        def load_miscellaneous_from_archive(self, archiver):
            pass

        def load_job_source_from_archive(self, archiver):
            self.archiver = archiver
            self.load_job_source_counter += 1

        def load_artifact_from_archive(self, archiver):
            self.archiver = archiver
            self.load_artifact_counter += 1

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def pipeline_context(self):
        return PipelineContext()

    def test_file_name_raises_exception_when_not_yet_defined(self):
        with self.assertRaises(ValueError) as error_context:
            self.pipeline_context.file_name

        self.assertIn(
            "Job ID is currently undefined, please set before retrieving",
            error_context.exception.args,
        )

    def test_file_name_returns_job_id(self):
        self.pipeline_context.file_name = self.job_id
        self.assertEqual(self.job_id, self.pipeline_context.file_name)

    def test_job_id_returns_job_id(self):
        self.pipeline_context.file_name = self.job_id
        self.assertEqual(self.job_id, self.pipeline_context.job_id)
