"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import unittest

from foundations_internal.scheduler import Scheduler
from foundations_contrib.scheduler_legacy_backend import LegacyBackend


class TestScheduler(unittest.TestCase):
    class MockBackend(LegacyBackend):
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

    class BadBackend(object):
        def __init__(self):
            pass

    def _make_job(self, job_name, status):
        from foundations.scheduler_job_information import JobInformation
        return JobInformation(job_name, 0, 0, status, "")

    def _prep_scheduler(self, queued_names, running_names, completed_names):
        queued_jobs = [self._make_job(queued_name, "QUEUED")
                       for queued_name in queued_names]
        running_jobs = [self._make_job(running_name, "RUNNING")
                        for running_name in running_names]
        completed_jobs = [self._make_job(
            completed_name, "COMPLETED") for completed_name in completed_names]

        backend = TestScheduler.MockBackend(
            queued_jobs, running_jobs, completed_jobs)

        return Scheduler(backend)

    def test_returns_non_list_iterable(self):
        scheduler = self._prep_scheduler([], [], [])

        jobs = scheduler.get_job_information()
        self.assertTrue(hasattr(jobs, "__iter__")
                        and not isinstance(jobs, list))

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
        self.assertEqual(
            queued_jobs, [self._make_job("another_job", "QUEUED")])

    def test_queued_jobs_two_jobs(self):
        scheduler = self._prep_scheduler(["one_job", "another_job"], [], [])

        queued_jobs = list(scheduler.get_job_information(status="QUEUED"))
        expected_queued_jobs = [self._make_job(
            "one_job", "QUEUED"), self._make_job("another_job", "QUEUED")]
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
        self.assertEqual(
            running_jobs, [self._make_job("another_job", "RUNNING")])

    def test_running_jobs_two_jobs(self):
        scheduler = self._prep_scheduler([], ["one_job", "another_job"], [])

        running_jobs = list(scheduler.get_job_information(status="RUNNING"))
        expected_running_jobs = [self._make_job(
            "one_job", "RUNNING"), self._make_job("another_job", "RUNNING")]
        self.assertEqual(running_jobs, expected_running_jobs)

    def test_get_completed_jobs_no_jobs(self):
        scheduler = self._prep_scheduler([], [], [])

        completed_jobs = list(
            scheduler.get_job_information(status="COMPLETED"))
        self.assertEqual(completed_jobs, [])

    def test_completed_jobs_one_job(self):
        scheduler = self._prep_scheduler([], [], ["one_job"])

        completed_jobs = list(
            scheduler.get_job_information(status="COMPLETED"))
        self.assertEqual(completed_jobs, [
                         self._make_job("one_job", "COMPLETED")])

    def test_completed_jobs_different_job(self):
        scheduler = self._prep_scheduler([], [], ["another_job"])

        completed_jobs = list(
            scheduler.get_job_information(status="COMPLETED"))
        self.assertEqual(completed_jobs, [
                         self._make_job("another_job", "COMPLETED")])

    def test_completed_jobs_two_jobs(self):
        scheduler = self._prep_scheduler([], [], ["one_job", "another_job"])

        completed_jobs = list(
            scheduler.get_job_information(status="COMPLETED"))
        expected_completed_jobs = [self._make_job(
            "one_job", "COMPLETED"), self._make_job("another_job", "COMPLETED")]
        self.assertEqual(completed_jobs, expected_completed_jobs)

    def test_all_jobs(self):
        scheduler = self._prep_scheduler(
            ["qj_0", "qj_1"], ["rj_0"], ["cj_0", "cj_1"])

        all_jobs = list(scheduler.get_job_information())
        expected_queued_jobs = [self._make_job(
            "qj_0", "QUEUED"), self._make_job("qj_1", "QUEUED")]
        expected_running_jobs = [self._make_job("rj_0", "RUNNING")]
        expected_completed_jobs = [self._make_job(
            "cj_0", "COMPLETED"), self._make_job("cj_1", "COMPLETED")]
        self.assertEqual(all_jobs, expected_queued_jobs +
                         expected_running_jobs + expected_completed_jobs)

    def test_all_jobs_different_arrangement(self):
        scheduler = self._prep_scheduler(
            [], ["rj_0", "rj_1"], ["cj_0", "cj_1", "cj_2"])

        all_jobs = list(scheduler.get_job_information())
        expected_queued_jobs = []
        expected_running_jobs = [self._make_job(
            "rj_0", "RUNNING"), self._make_job("rj_1", "RUNNING")]
        expected_completed_jobs = [self._make_job("cj_0", "COMPLETED"), self._make_job(
            "cj_1", "COMPLETED"), self._make_job("cj_2", "COMPLETED")]
        self.assertEqual(all_jobs, expected_queued_jobs +
                         expected_running_jobs + expected_completed_jobs)

    def test_unsupported_backend(self):
        with self.assertRaises(TypeError):
            scheduler = Scheduler(TestScheduler.BadBackend())
