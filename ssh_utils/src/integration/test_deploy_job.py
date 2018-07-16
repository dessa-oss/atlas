"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest


class TestDeployJob(unittest.TestCase):

    def setUp(self):
        from integration.cleanup import cleanup
        cleanup()

    def test_can_deploy_job_remotely(self):
        from vcat import pipeline
        from os.path import isfile
        from integration.config import code_path

        def method():
            pass

        stage = pipeline.stage(method)
        deployment = self._make_deployment(stage)
        deployment.deploy()

        job_path = '{}/{}.tgz'.format(code_path(), deployment.job_name())
        self.assertTrue(isfile(job_path))

    def test_can_fetch_job_results(self):
        from vcat import pipeline

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
        from vcat import pipeline, JobPersister, ResultReader

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

    def _run_worker(self):
        from vcat import SimpleWorker
        from integration.config import code_path, result_path

        SimpleWorker(code_path(), result_path()).run_once(set())

    def _make_deployment(self, stage, **kwargs):
        from vcat_ssh import SFTPJobDeployment
        from vcat import Job, JobSourceBundle
        from integration.config import DEPLOYMENT_CONFIG
        from uuid import uuid4

        job = Job(stage, **kwargs)
        job_name = str(uuid4())
        source_bundle = JobSourceBundle.for_deployment()

        deployment = SFTPJobDeployment(job_name, job, source_bundle)
        deployment.config().update(DEPLOYMENT_CONFIG)
        return deployment
