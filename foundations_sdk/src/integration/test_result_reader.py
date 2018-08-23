"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations import Pipeline, PipelineContext, Job, JobPersister, ResultReader


class TestResultReader(unittest.TestCase):

    def test_creates_job_information(self):
        def method():
            pass

        stage = self._make_pipeline().stage(method)
        self._run_and_persist(stage)

        job_information = self._create_reader_and_get_job_information(stage)
        self.assertFalse(job_information.empty)

    def test_multiple_runs_do_not_break(self):
        def method():
            pass

        def method2():
            pass

        pipeline = self._make_pipeline()

        stage = pipeline.stage(method)
        self._run_and_persist(stage)

        stage2 = pipeline.stage(method2)
        self._run_and_persist(stage2)

        job_information = self._create_reader_and_get_job_information(stage)
        self.assertFalse(job_information.empty)

        job_information = self._create_reader_and_get_job_information(stage2)
        self.assertFalse(job_information.empty)

    def test_stores_hierarchy(self):
        def method():
            pass

        pipeline = self._make_pipeline()
        stage = pipeline.stage(method)
        self._run_and_persist(stage)

        job_information = self._create_reader_and_get_job_information(stage)
        parent_list = job_information['parent_ids'].iloc[0]
        self.assertIn(pipeline.uuid(), parent_list)

    def test_stores_stage_name(self):
        def method():
            pass

        stage = self._make_pipeline().stage(method)
        self._run_and_persist(stage)

        job_information = self._create_reader_and_get_job_information(stage)
        stage_name = job_information['stage_name'].iloc[0]
        self.assertEqual('method', stage_name)

    def test_stores_stage_uuid(self):
        def method():
            pass

        stage = self._make_pipeline().stage(method)
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
        return job_information[job_information['pipeline_name'] == job_name]

    def _run_and_persist(self, stage):
        stage.run_same_process()
        self._persist_stage(stage)

    def _make_pipeline(self):
        return Pipeline(PipelineContext())

    def _persist_stage(self, stage):
        persister = self._make_persister(stage)
        persister.persist()

    def _make_persister(self, stage, **kwargs):
        job = Job(stage, **kwargs)
        return JobPersister(job)
