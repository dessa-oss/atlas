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
        from integration.config import make_code_bucket
        from vcat_gcp import GCPBucket

        def method():
            pass

        stage = pipeline.stage(method)
        deployment = self._make_deployment(stage)
        deployment.deploy()

        bucket = make_code_bucket()
        code_path = '{}.tgz'.format(deployment.job_name())
        self.assertTrue(bucket.exists(code_path))

    def _make_deployment(self, stage, **kwargs):
        from vcat import Job, JobSourceBundle, BucketJobDeployment
        from uuid import uuid4
        from integration.config import make_code_bucket, make_result_bucket

        job = Job(stage, **kwargs)
        job_name = str(uuid4())
        source_bundle = JobSourceBundle.for_deployment()

        return BucketJobDeployment(job_name, job, source_bundle, make_code_bucket(), make_result_bucket())
