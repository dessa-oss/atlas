"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest


class TestDeployJob(unittest.TestCase):

    def setUp(self):
        from acceptance.cleanup import cleanup
        cleanup()

    def test_can_fetch_job_results(self):
        from foundations import pipeline

        def method():
            return 27

        stage = pipeline.stage(method)
        stage.persist()
        deployment = self._make_deployment(stage)
        deployment.deploy()

        self._run_worker()
        results = deployment.fetch_job_results()

        self.assertEqual(27, results['stage_contexts']
                         [stage.uuid()]['stage_output'])

    def test_can_fetch_job_info(self):
        from foundations import pipeline, JobPersister, ResultReader

        def method():
            pass

        stage = pipeline.stage(method)
        stage.persist()
        deployment = self._make_deployment(stage)
        deployment.deploy()

        self._run_worker()
        with JobPersister.load_archiver_fetch() as archiver:
            reader = ResultReader(archiver)
            job_information = reader.get_job_information()
            current_job_information = job_information[job_information['pipeline_name'] == deployment.job_name()].iloc[0]
            self.assertIsNotNone(current_job_information)

    def test_can_fetch_results(self):
        from foundations import pipeline, JobPersister, ResultReader

        def method():
            pass

        stage = pipeline.stage(method)
        stage.persist()
        deployment = self._make_deployment(stage)
        deployment.deploy()

        self._run_worker()
        with JobPersister.load_archiver_fetch() as archiver:
            reader = ResultReader(archiver)
            results = reader.get_results()
            current_results = results[results['pipeline_name'] == deployment.job_name()].iloc[0]
            self.assertIsNotNone(current_results)

    def test_can_fetch_results_multiple_jobs(self):
        from foundations import pipeline, JobPersister, ResultReader

        def method():
            pass

        stage = pipeline.stage(method)
        stage.persist()

        deployment = self._make_deployment(stage)
        deployment.deploy()

        deployment2 = self._make_deployment(stage)
        deployment2.deploy()

        self._run_worker()
        with JobPersister.load_archiver_fetch() as archiver:
            reader = ResultReader(archiver)
            results = reader.get_results()

            current_results = results[results['pipeline_name'] == deployment.job_name()].iloc[0]
            self.assertIsNotNone(current_results)

            current_results2 = results[results['pipeline_name'] == deployment2.job_name()].iloc[0]
            self.assertIsNotNone(current_results2)

    def _run_worker(self):
        from foundations import SimpleWorker
        from acceptance.config import code_path, result_path

        SimpleWorker(code_path(), result_path()).run_once(set())

    def _make_deployment(self, stage, **kwargs):
        from foundations_ssh import SFTPJobDeployment
        from foundations import Job, JobSourceBundle
        from acceptance.config import DEPLOYMENT_CONFIG
        from uuid import uuid4

        job = Job(stage, **kwargs)
        job_name = str(uuid4())
        source_bundle = JobSourceBundle.for_deployment()

        deployment = SFTPJobDeployment(job_name, job, source_bundle)
        deployment.config().update(DEPLOYMENT_CONFIG)
        return deployment
