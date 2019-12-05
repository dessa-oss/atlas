"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest


class TestDuplicateJobSource(unittest.TestCase):

    def setUp(self):
        from acceptance.cleanup import cleanup
        cleanup()

    def test_can_duplicate_job_source(self):
        from acceptance.config import TEST_UUID
        from foundations import JobPersister, ResultReader
        from foundations.global_state import foundations_context

        def method():
            pass

        stage = foundations_context.pipeline().stage(method)
        stage.persist()

        deployment = self._make_deployment(stage)
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
        from foundations import SimpleBucketWorker
        from acceptance.config import make_code_bucket, make_result_bucket

        SimpleBucketWorker(make_code_bucket(), make_result_bucket()).run_once(set())

    def _make_deployment(self, stage, **kwargs):
        from foundations import Job, DeploymentWrapper, BucketJobDeployment
        from foundations_contrib.job_source_bundle import JobSourceBundle
        from uuid import uuid4
        from acceptance.config import make_code_bucket, make_result_bucket

        job = Job(stage, **kwargs)
        job_name = str(uuid4())
        source_bundle = JobSourceBundle.for_deployment()

        inner_deployment = BucketJobDeployment(job_name, job, source_bundle, make_code_bucket(), make_result_bucket())
        inner_deployment.deploy()
        return DeploymentWrapper(inner_deployment)
