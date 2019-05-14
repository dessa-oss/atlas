"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_internal.pipeline import Pipeline
from foundations_internal.pipeline_context import PipelineContext
from foundations import Job, JobPersister, ResultReader


class TestResultReader(Spec):

    @let
    def job_pipeline(self):
        return Pipeline(self.pipeline_context_with_job_id)

    @let
    def pipeline_context_with_job_id(self):
        context =  PipelineContext()
        context.file_name = self.job_uuid
        return context

    @let
    def job_uuid(self):
        return self.faker.uuid4()

    def test_creates_job_information(self):
        def method():
            pass

        stage = self.job_pipeline.stage(method)
        self._run_and_persist(stage)

        job_information = self._create_reader_and_get_job_information(stage)
        self.assertFalse(job_information.empty)

    def test_multiple_runs_do_not_break(self):
        def method():
            pass

        def method2():
            pass

        stage = self.job_pipeline.stage(method)
        self._run_and_persist(stage)

        stage2 = self.job_pipeline.stage(method2)
        self._run_and_persist(stage2)

        job_information = self._create_reader_and_get_job_information(stage)
        self.assertFalse(job_information.empty)

        job_information = self._create_reader_and_get_job_information(stage2)
        self.assertFalse(job_information.empty)

    def test_stores_hierarchy(self):
        def method():
            pass

        stage = self.job_pipeline.stage(method)
        self._run_and_persist(stage)

        job_information = self._create_reader_and_get_job_information(stage)
        parent_list = job_information['parent_ids'].iloc[0]
        self.assertIn(self.job_pipeline.uuid(), parent_list)

    def test_stores_stage_name(self):
        def method():
            pass

        stage = self.job_pipeline.stage(method)
        self._run_and_persist(stage)

        job_information = self._create_reader_and_get_job_information(stage)
        stage_name = job_information['stage_name'].iloc[0]
        self.assertEqual('method', stage_name)

    def test_stores_stage_uuid(self):
        def method():
            pass

        stage = self.job_pipeline.stage(method)
        self._run_and_persist(stage)

        job_information = self._create_reader_and_get_job_information(stage)
        stage_uuid = job_information['stage_id'].iloc[0]
        self.assertEqual(stage.uuid(), stage_uuid)

    def _create_reader_and_get_job_information(self, stage):
        with JobPersister.load_archiver_fetch() as archiver:
            reader = ResultReader(archiver)
            return self._get_job_information(reader, stage)

    def _get_job_information(self, reader, stage):
        job_name = stage.pipeline_context().file_name
        job_information = reader.get_job_information()
        return job_information[job_information['job_name'] == job_name]

    def _run_and_persist(self, stage):
        stage.run_same_process()
        self._persist_stage(stage)

    def _persist_stage(self, stage):
        persister = self._make_persister(stage)
        persister.persist()

    def _make_persister(self, stage, **kwargs):
        job = Job(stage, **kwargs)
        return JobPersister(job)
