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
        from foundations.global_state import foundations_context
        from os.path import isfile
        from integration.config import code_path

        def method():
            pass

        stage = foundations_context.pipeline().stage(method)
        deployment = self._make_deployment(stage)
        deployment.deploy()

        job_path = '{}/{}.tgz'.format(code_path(), deployment.job_name())
        self.assertTrue(isfile(job_path))

    def _make_deployment(self, stage, **kwargs):
        from foundations_ssh import SFTPJobDeployment
        from foundations import Job, JobSourceBundle
        from integration.config import DEPLOYMENT_CONFIG
        from uuid import uuid4

        job = Job(stage, **kwargs)
        job_name = str(uuid4())
        source_bundle = JobSourceBundle.for_deployment()

        deployment = SFTPJobDeployment(job_name, job, source_bundle)
        deployment.config().update(DEPLOYMENT_CONFIG)
        return deployment
