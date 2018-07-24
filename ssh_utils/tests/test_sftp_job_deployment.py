"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
import ssh_utils_fixtures.sftp_job_deployment_fixtures as sjf
import foundations.constants as constants

class TestSFTPJobDeployment(unittest.TestCase):
    def test_job_queued(self):
        queued = sjf.QueuedMockDeployment()

        self.assertEqual(constants.deployment_queued, queued.get_job_status())

    def test_job_never_finishes(self):
        never_done = sjf.NeverFinishDeployment()

        self.assertEqual(constants.deployment_running, never_done.get_job_status())
        
    def test_job_completed_instantly(self):
        done = sjf.SuccessfulMockDeployment()

        self.assertEqual(constants.deployment_completed, done.get_job_status())

    def test_job_failed_instantly(self):
        failed = sjf.FailedMockDeployment()

        self.assertEqual(constants.deployment_error, failed.get_job_status())

    def test_takes_one_second(self):
        deploy = sjf.TakesOneSecond()

        for _ in range(0, 1):
            self.assertEqual(constants.deployment_running, deploy.get_job_status())

        self.assertEqual(constants.deployment_completed, deploy.get_job_status())
        self.assertEqual(constants.deployment_completed, deploy.get_job_status())

    def test_takes_two_seconds(self):
        deploy = sjf.TakesTwoSeconds()

        for _ in range(0, 2):
            self.assertEqual(constants.deployment_running, deploy.get_job_status())

        self.assertEqual(constants.deployment_completed, deploy.get_job_status())
        self.assertEqual(constants.deployment_completed, deploy.get_job_status())

    def test_takes_random_time(self):
        deploy = sjf.SuccessfulTakesRandomTime()

        while deploy.get_job_status() == constants.deployment_running:
            pass

        self.assertEqual(constants.deployment_completed, deploy.get_job_status())
        self.assertEqual(constants.deployment_completed, deploy.get_job_status())

    def test_fails_random_time(self):
        deploy = sjf.FailedTakesRandomTime()

        while deploy.get_job_status() == constants.deployment_running:
            pass

        self.assertEqual(constants.deployment_error, deploy.get_job_status())
        self.assertEqual(constants.deployment_error, deploy.get_job_status())