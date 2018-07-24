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

    def test_can_duplicate_job_source(self):
        from acceptance.config import TEST_UUID
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
            duplicate_path = 'tmp/duplicate_jobs_{}'.format(TEST_UUID)
            reader.create_working_copy(deployment.job_name(), duplicate_path)

            with open(__file__, 'r') as file:
                expected_content = file.read()

            with open('{}/acceptance/test_duplicate_job_source.py'.format(duplicate_path), 'r') as file:
                result_content = file.read()

            self.assertEqual(expected_content, result_content)

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
