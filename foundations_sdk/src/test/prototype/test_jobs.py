"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers.conditional_return import ConditionalReturn
from foundations_internal.testing.helpers import *
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal
from uuid import uuid4

from foundations.prototype.jobs import *

class TestPrototypeJobs(Spec):

    all_queued_jobs_mock = let_patch_mock('foundations_contrib.models.queued_job.QueuedJob.all')

    @let_now
    def redis(self):
        from fakeredis import FakeRedis
        redis = FakeRedis()
        redis.flushall()
        return self.patch('foundations_contrib.global_state.redis_connection', redis)

    @let
    def job_id(self):
        return self._random_uuid()

    @let
    def job_id_two(self):
        return self._random_uuid()

    def test_archive_jobs_returns_empty_when_no_jobs(self):
        result = archive_jobs([])
        self.assertEqual({}, result)

    def test_archive_jobs_returns_job_mapped_to_false_when_job_does_not_exist(self):
        result = archive_jobs([self.job_id])
        self.assertEqual({self.job_id: False}, result)

    def test_archive_jobs_returns_job_mapped_to_false_when_job_does_not_exist_with_multiple_jobs(self):
        result = archive_jobs([self.job_id, self.job_id_two])
        self.assertEqual({self.job_id: False, self.job_id_two: False}, result)

    def test_archive_jobs_returns_job_mapped_to_true_when_job_exists(self):
        self._track_completed_job(self.job_id)
        result = archive_jobs([self.job_id])
        self.assertEqual({self.job_id: True}, result)

    def test_archive_jobs_removes_completed_jobs(self):
        self._track_completed_job(self.job_id)
        archive_jobs([self.job_id])
        result = archive_jobs([self.job_id])
        self.assertEqual({self.job_id: False}, result)

    def test_archive_jobs_archives_completed_jobs(self):
        from foundations.prototype.helpers.completed import list_archived_jobs

        self._track_completed_job(self.job_id)
        archive_jobs([self.job_id, self.job_id_two])
        result = list_archived_jobs(self.redis)
        self.assertEqual({self.job_id, self.job_id_two}, result)

    def test_archive_jobs_returns_job_mapped_to_true_when_job_exists_with_multiple_jobs(self):
        self._track_completed_job(self.job_id)
        self._track_completed_job(self.job_id_two)
        result = archive_jobs([self.job_id, self.job_id_two])
        self.assertEqual({self.job_id: True, self.job_id_two: True}, result)

    def test_archive_jobs_returns_job_mapped_to_true_when_job_exists_with_multiple_jobs_only_one_exists(self):
        self._track_completed_job(self.job_id_two)
        result = archive_jobs([self.job_id, self.job_id_two])
        self.assertEqual({self.job_id: False, self.job_id_two: True}, result)

    def test_archive_jobs_is_global(self):
        import foundations.prototype
        self.assertEqual(archive_jobs, foundations.prototype.archive_jobs)
    
    def test_get_queued_jobs_returns_empty_data_frame(self):
        self.all_queued_jobs_mock.return_value = []

        expected_result = DataFrame([])
        assert_frame_equal(expected_result, get_queued_jobs())

    def test_get_queued_jobs_returns_a_queued_job(self):
        first_queued_job = self._random_queued_job()
        
        self.all_queued_jobs_mock.return_value = [first_queued_job]
        
        expected_result = DataFrame([
            {
                'job_id': first_queued_job.job_id,
                'queued_time': first_queued_job.queued_time,
                'time_since_queued': first_queued_job.time_since_queued,
                'project_name': first_queued_job.project_name,
            }
        ])
        assert_frame_equal(expected_result, get_queued_jobs())

    def test_get_queued_jobs_returns_queued_jobs(self):
        first_queued_job = self._random_queued_job()
        second_queued_job = self._random_queued_job()
        
        self.all_queued_jobs_mock.return_value = [first_queued_job, second_queued_job]
        
        expected_result = DataFrame([
            {
                'job_id': first_queued_job.job_id,
                'queued_time': first_queued_job.queued_time,
                'time_since_queued': first_queued_job.time_since_queued,
                'project_name': first_queued_job.project_name,
            },
            {
                'job_id': second_queued_job.job_id,
                'queued_time': second_queued_job.queued_time,
                'time_since_queued': second_queued_job.time_since_queued,
                'project_name': second_queued_job.project_name,
            }
        ])
        assert_frame_equal(expected_result, get_queued_jobs())
        
    def test_get_queued_jobs_is_global(self):
        import foundations.prototype
        self.assertEqual(get_queued_jobs, foundations.prototype.get_queued_jobs)
    
    def _track_completed_job(self, job_id):
        self.redis.sadd('projects:global:jobs:completed', job_id)

    def _random_queued_job(self):
        from foundations_contrib.models.queued_job import QueuedJob
        import random

        return QueuedJob(
            job_id=self.faker.sha256(),
            queued_time=random.randint(1, 100),
            time_since_queued=random.randint(1, 100),
            project_name=self.faker.name()
        )
    
    @staticmethod
    def _random_uuid():
        from uuid import uuid4
        return str(uuid4())