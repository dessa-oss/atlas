"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
import foundations_sdk_fixtures.local_shell_job_deployment_fixtures as lsf
import foundations.constants as constants

class TestLocalShellJobDeployment(unittest.TestCase):
    def test_job_completed_instantly(self):
        done = lsf.SuccessfulMockDeployment()

        self.assertEqual(constants.deployment_completed, done.get_job_status())

    def test_job_failed_instantly(self):
        failed = lsf.FailedMockDeployment()

        self.assertEqual(constants.deployment_error, failed.get_job_status())