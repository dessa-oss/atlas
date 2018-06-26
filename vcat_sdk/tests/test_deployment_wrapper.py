"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from vcat.deployment_wrapper import DeploymentWrapper
import fixtures.deployment_wrapper_fixtures as dwf

class TestDeploymentWrapper(unittest.TestCase):
    def test_get_job_name(self):
        job_name = "job_name"

        deployment = DeploymentWrapper(dwf.MockDeployment(job_name))
        self.assertEqual(job_name, deployment.job_name())

    def test_get_different_job_name(self):
        job_name = "diff_name"

        deployment = DeploymentWrapper(dwf.MockDeployment(job_name))
        self.assertEqual(job_name, deployment.job_name())

    def test_is_job_complete_instantly_complete(self):
        deployment = DeploymentWrapper(dwf.InstantFinishDeployment("job_name"))
        self.assertTrue(deployment.is_job_complete())

    def test_is_job_complete_never_finish(self):
        deployment = DeploymentWrapper(dwf.NeverFinishDeployment("job_name"))
        self.assertFalse(deployment.is_job_complete())

    def test_is_job_complete_takes_one_second(self):
        deployment = DeploymentWrapper(dwf.TakesOneSecond("job_name"))

        for _ in range(0, 1):
            self.assertFalse(deployment.is_job_complete())

        self.assertTrue(deployment.is_job_complete())