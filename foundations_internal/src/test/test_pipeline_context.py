
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

    def test_fill_provenance(self):
        from foundations_contrib.config_manager import ConfigManager

        self.config_manager = ConfigManager()
        pipeline_context = PipelineContext()

        self.config_manager["other_world"] = "aliens"

        pipeline_context.fill_provenance(self.config_manager)
        self.assertEqual(pipeline_context.provenance.config["other_world"], "aliens")

    def test_save_uses_save_method_on_result_saver(self):
        pipeline_context = PipelineContext()
        pipeline_context.file_name = self.job_id
        mock_result_saver = self.MockResultSaver()

        pipeline_context.save(mock_result_saver)
        self.assertEqual(mock_result_saver.file_name, pipeline_context.file_name)
        self.assertEqual(mock_result_saver.context, pipeline_context._context())

    def test_load_provenance_from_archive(self):
        pipeline_context = PipelineContext()
        mock_archive = self.MockArchive()

        pipeline_context.load_provenance_from_archive(mock_archive)

    def test_load_provenance_from_archive_with_mock_provenance(self):
        pipeline_context = PipelineContext()
        mock_archive = self.MockArchive()
        mock_provenance = self.MockProvenance()

        pipeline_context.provenance = mock_provenance
        pipeline_context.load_provenance_from_archive(mock_archive)

        self.assertEqual(mock_archive, mock_provenance.archiver)

    def test_load_provenance_from_archive_fully_loaded(self):
        pipeline_context = PipelineContext()
        mock_archive = self.MockArchive()
        mock_provenance = self.MockProvenance()

        pipeline_context.mark_fully_loaded()
        pipeline_context.provenance = mock_provenance
        pipeline_context.load_provenance_from_archive(mock_archive)

        self.assertEqual(0, mock_provenance.load_provenace_counter)

    def test_load_job_source_from_archive(self):
        pipeline_context = PipelineContext()
        mock_archive = self.MockArchive()

        pipeline_context.load_job_source_from_archive(mock_archive)

    def test_load_job_source_from_archive_with_mock_provenance(self):
        pipeline_context = PipelineContext()
        mock_archive = self.MockArchive()
        mock_provenance = self.MockProvenance()

        pipeline_context.provenance = mock_provenance
        pipeline_context.load_job_source_from_archive(mock_archive)

        self.assertEqual(mock_archive, mock_provenance.archiver)

    def test_load_job_source_from_archive_fully_loaded(self):
        pipeline_context = PipelineContext()
        mock_archive = self.MockArchive()
        mock_provenance = self.MockProvenance()

        pipeline_context.mark_fully_loaded()
        pipeline_context.provenance = mock_provenance
        pipeline_context.load_job_source_from_archive(mock_archive)

        self.assertEqual(0, mock_provenance.load_job_source_counter)

    def test_load_artifact_from_archive(self):
        pipeline_context = PipelineContext()
        mock_archive = self.MockArchive()

        pipeline_context.load_artifact_from_archive(mock_archive)

    def test_load_artifact_from_archive_with_mock_provenance(self):
        pipeline_context = PipelineContext()
        mock_archive = self.MockArchive()
        mock_provenance = self.MockProvenance()

        pipeline_context.provenance = mock_provenance
        pipeline_context.load_artifact_from_archive(mock_archive)

        self.assertEqual(mock_archive, mock_provenance.archiver)

    def test_load_artifact_from_archive_fully_loaded(self):
        pipeline_context = PipelineContext()
        mock_archive = self.MockArchive()
        mock_provenance = self.MockProvenance()

        pipeline_context.mark_fully_loaded()
        pipeline_context.provenance = mock_provenance
        pipeline_context.load_artifact_from_archive(mock_archive)

        self.assertEqual(0, mock_provenance.load_artifact_counter)
