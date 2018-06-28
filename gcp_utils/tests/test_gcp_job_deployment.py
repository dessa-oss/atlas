"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
import gcp_utils_fixtures.gcp_job_deployment_fixtures as gcf

class TestGCPJobDeployment(unittest.TestCase):
    def test_job_never_finishes(self):
        never_done = gcf.NeverFinishDeployment()

        self.assertEqual("Running", never_done.get_job_status())
        
    def test_job_completed_instantly(self):
        done = gcf.SuccessfulMockDeployment()

        self.assertEqual("Completed", done.get_job_status())

    def test_job_failed_instantly(self):
        failed = gcf.FailedMockDeployment()

        self.assertEqual("Error", failed.get_job_status())

    def test_takes_one_second(self):
        deploy = gcf.TakesOneSecond()

        for _ in range(0, 1):
            self.assertEqual("Running", deploy.get_job_status())

        self.assertEqual("Completed", deploy.get_job_status())
        self.assertEqual("Completed", deploy.get_job_status())

    def test_takes_two_seconds(self):
        deploy = gcf.TakesTwoSeconds()

        for _ in range(0, 2):
            self.assertEqual("Running", deploy.get_job_status())

        self.assertEqual("Completed", deploy.get_job_status())
        self.assertEqual("Completed", deploy.get_job_status())

    def test_takes_random_time(self):
        deploy = gcf.SuccessfulTakesRandomTime()

        while deploy.get_job_status() == "Running":
            pass

        self.assertEqual("Completed", deploy.get_job_status())
        self.assertEqual("Completed", deploy.get_job_status())

    def test_fails_random_time(self):
        deploy = gcf.FailedTakesRandomTime()

        while deploy.get_job_status() == "Running":
            pass

        self.assertEqual("Error", deploy.get_job_status())
        self.assertEqual("Error", deploy.get_job_status())