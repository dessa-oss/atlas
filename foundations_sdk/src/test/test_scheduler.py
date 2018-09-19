"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import unittest

from foundations.scheduler import Scheduler

class TestScheduler(unittest.TestCase):
    class MockBackend(object):
        def __init__(self, queued_jobs, running_jobs, completed_jobs):
            self._queued_jobs = queued_jobs
            self._running_jobs = running_jobs
            self._completed_jobs = completed_jobs

        def get_paginated(self, start_index, number_to_get, status):
            if status == "QUEUED":
                return self._queued_jobs
            
            if status == "RUNNING":
                return self._running_jobs

            if status == "COMPLETED":
                return self._completed_jobs

            return self._queued_jobs + self._running_jobs + self._completed_jobs

    def _make_job(self, job_name, status):
        from foundations.scheduler_job_information import JobInformation
        return JobInformation(job_name, 0, 0, status, "")

    def _prep_scheduler(self, queued_names, running_names, completed_names):
        queued_jobs = [self._make_job(queued_name, "QUEUED") for queued_name in queued_names]
        running_jobs = [self._make_job(running_name, "RUNNING") for running_name in running_names]
        completed_jobs = [self._make_job(completed_name, "COMPLETED") for completed_name in completed_names]

        backend = TestScheduler.MockBackend(queued_jobs, running_jobs, completed_jobs)

        return Scheduler(backend)

    def test_get_queued_jobs_no_jobs(self):
        scheduler = self._prep_scheduler([], [], [])

        queued_jobs = list(scheduler.get_job_information(status="QUEUED"))
        self.assertEqual(queued_jobs, [])

    def test_queued_jobs_one_job(self):
        scheduler = self._prep_scheduler(["one_job"], [], [])

        queued_jobs = list(scheduler.get_job_information(status="QUEUED"))
        self.assertEqual(queued_jobs, [self._make_job("one_job", "QUEUED")])

    def test_queued_jobs_different_job(self):
        scheduler = self._prep_scheduler(["another_job"], [], [])

        queued_jobs = list(scheduler.get_job_information(status="QUEUED"))
        self.assertEqual(queued_jobs, [self._make_job("another_job", "QUEUED")])

    def test_queued_jobs_two_jobs(self):
        scheduler = self._prep_scheduler(["one_job", "another_job"], [], [])

        queued_jobs = list(scheduler.get_job_information(status="QUEUED"))
        expected_queued_jobs = [self._make_job("one_job", "QUEUED"), self._make_job("another_job", "QUEUED")]
        self.assertEqual(queued_jobs, expected_queued_jobs)

    def test_get_running_jobs_no_jobs(self):
        scheduler = self._prep_scheduler([], [], [])

        running_jobs = list(scheduler.get_job_information(status="RUNNING"))
        self.assertEqual(running_jobs, [])

    def test_running_jobs_one_job(self):
        scheduler = self._prep_scheduler([], ["one_job"], [])

        running_jobs = list(scheduler.get_job_information(status="RUNNING"))
        self.assertEqual(running_jobs, [self._make_job("one_job", "RUNNING")])

    def test_running_jobs_different_job(self):
        scheduler = self._prep_scheduler([], ["another_job"], [])

        running_jobs = list(scheduler.get_job_information(status="RUNNING"))
        self.assertEqual(running_jobs, [self._make_job("another_job", "RUNNING")])

    def test_running_jobs_two_jobs(self):
        scheduler = self._prep_scheduler([], ["one_job", "another_job"], [])

        running_jobs = list(scheduler.get_job_information(status="RUNNING"))
        expected_running_jobs = [self._make_job("one_job", "RUNNING"), self._make_job("another_job", "RUNNING")]
        self.assertEqual(running_jobs, expected_running_jobs)

    def test_get_completed_jobs_no_jobs(self):
        scheduler = self._prep_scheduler([], [], [])

        completed_jobs = list(scheduler.get_job_information(status="COMPLETED"))
        self.assertEqual(completed_jobs, [])

    def test_completed_jobs_one_job(self):
        scheduler = self._prep_scheduler([], [], ["one_job"])

        completed_jobs = list(scheduler.get_job_information(status="COMPLETED"))
        self.assertEqual(completed_jobs, [self._make_job("one_job", "COMPLETED")])

    def test_completed_jobs_different_job(self):
        scheduler = self._prep_scheduler([], [], ["another_job"])

        completed_jobs = list(scheduler.get_job_information(status="COMPLETED"))
        self.assertEqual(completed_jobs, [self._make_job("another_job", "COMPLETED")])

    def test_completed_jobs_two_jobs(self):
        scheduler = self._prep_scheduler([], [], ["one_job", "another_job"])

        completed_jobs = list(scheduler.get_job_information(status="COMPLETED"))
        expected_completed_jobs = [self._make_job("one_job", "COMPLETED"), self._make_job("another_job", "COMPLETED")]
        self.assertEqual(completed_jobs, expected_completed_jobs)