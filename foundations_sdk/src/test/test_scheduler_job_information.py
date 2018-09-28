"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import unittest

from foundations.scheduler_job_information import JobInformation

class TestSchedulerJobInformation(unittest.TestCase):
    def test_uuid(self):
        job_information = JobInformation("this_job", 0, 0, "", "")
        self.assertEqual(job_information.uuid(), "this_job")

    def test_uuid_different_uuid(self):
        job_information = JobInformation("that_job", 0, 0, "", "")
        self.assertEqual(job_information.uuid(), "that_job")

    def test_user_submitted(self):
        job_information = JobInformation("", 0, 0, "", "me")
        self.assertEqual(job_information.user_submitted(), "me")
    
    def test_user_submitted_different_user(self):
        job_information = JobInformation("", 0, 0, "", "you")
        self.assertEqual(job_information.user_submitted(), "you")

    def test_status(self):
        job_information = JobInformation("", 0, 0, "QUEUED", "")
        self.assertEqual(job_information.status(), "QUEUED")

    def test_status_different_status(self):
        job_information = JobInformation("", 0, 0, "RUNNING", "")
        self.assertEqual(job_information.status(), "RUNNING")

    def test_duration(self):
        job_information = JobInformation("", 0, 123, "", "")
        self.assertEqual(job_information.duration(), 123)

    def test_duration_different_duration(self):
        job_information = JobInformation("", 0, 456, "", "")
        self.assertEqual(job_information.duration(), 456)

    def test_submission_datetime(self):
        from datetime import datetime

        timestamp = 1537368209
        datetime_from_timestamp = datetime.utcfromtimestamp(timestamp)

        job_information = JobInformation("", timestamp, 0, "", "")

        self.assertEqual(job_information.submission_datetime(), datetime_from_timestamp)

    def test_submission_datetime_different_datetime(self):
        from datetime import datetime

        timestamp = 1336364321
        datetime_from_timestamp = datetime.utcfromtimestamp(timestamp)

        job_information = JobInformation("", timestamp, 0, "", "")

        self.assertEqual(job_information.submission_datetime(), datetime_from_timestamp)