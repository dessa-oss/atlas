"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from vcat import Pipeline, PipelineContext, Job, JobPersister, ResultReader


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

    def test_creates_job_results(self):
        def method():
            return None, {'score': 99.9}

        stage = self._make_pipeline().stage(method)
        self._run_and_persist(stage)

        job_results = self._create_reader_and_get_job_results(stage)
        self.assertFalse(job_results.empty)

    def test_stores_stage_results(self):
        def method():
            return None, {'score': 99.9}

        stage = self._make_pipeline().stage(method)
        self._run_and_persist(stage)

        job_results = self._create_reader_and_get_job_results(stage)
        stage_results = self._get_stage_results(job_results, stage)
        self.assertEqual(99.9, stage_results['score'])

    def test_stores_multiple_stage_results(self):
        def method():
            return None, {'score': 99.9, 'loss': 0.54}

        stage = self._make_pipeline().stage(method)
        self._run_and_persist(stage)

        job_results = self._create_reader_and_get_job_results(stage)
        stage_results = self._get_stage_results(job_results, stage)

        self.assertEqual(99.9, stage_results['score'])
        self.assertEqual(0.54, stage_results['loss'])

    def test_stores_stage_results_multiple_stages(self):
        def method():
            return None, {'score': 93.9}

        def method2(unused):
            return None, {'loss': 0.14}

        stage = self._make_pipeline().stage(method)
        stage2 = stage.stage(method2)
        self._run_and_persist(stage2)

        job_results = self._create_reader_and_get_job_results(stage)

        stage_results = self._get_stage_results(job_results, stage)
        self.assertEqual(93.9, stage_results['score'])

        stage_results = self._get_stage_results(job_results, stage2)
        self.assertEqual(0.14, stage_results['loss'])

    def _get_stage_results(self, job_results, stage):
        return job_results[job_results['stage_id'] == stage.uuid()].iloc[0]

    def _create_reader_and_get_job_results(self, stage):
        with JobPersister.load_archiver_fetch() as archiver:
            reader = ResultReader(archiver)
            return self._get_job_results(reader, stage)

    def _get_job_results(self, reader, stage):
        job_name = stage.pipeline_context().file_name
        job_results = reader.get_results()
        return job_results[job_results['pipeline_name'] == job_name]

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
