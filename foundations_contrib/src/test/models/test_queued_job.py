"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_internal.testing.helpers import let, let_patch_mock, let_patch_instance, set_up
from foundations_internal.testing.helpers.spec import Spec

from foundations_contrib.models.queued_job import QueuedJob

from fakeredis import FakeRedis


class TestQueuedJob(Spec):

    mock_time = let_patch_mock('time.time')

    mock_redis = let_patch_mock('foundations.global_state.redis_connection', FakeRedis())

    @let
    def mock_redis_pipeline(self):
        from foundations_contrib.redis_pipeline_wrapper import RedisPipelineWrapper
        
        pipeline = self.mock_redis.pipeline()
        return RedisPipelineWrapper(pipeline)

    @let
    def job_id(self):
        return self.faker.sha256()

    @let
    def queued_time(self):
        import random
        return random.randint(1, 100)

    @let
    def project_name(self):
        import uuid
        return str(uuid.uuid4())

    @let
    def time_since_queued(self):
        import random
        return random.randint(1, 100)

    @let
    def job_id_two(self):
        return self.faker.sha256()

    @let
    def queued_time_two(self):
        import random
        return random.randint(1, 100)

    @let
    def project_name_two(self):
        import uuid
        return str(uuid.uuid4())

    @let
    def time_since_queued_two(self):
        from time import time
        return time() - self.queued_time_two

    @let
    def queued_job(self):
        return QueuedJob(
            job_id=self.job_id,
            queued_time=self.queued_time,
            project_name=self.project_name,
            time_since_queued=self.time_since_queued
        )

    @let
    def queued_job_two(self):
        return QueuedJob(
            job_id=self.job_id_two,
            queued_time=self.queued_time_two,
            project_name=self.project_name_two,
            time_since_queued=self.time_since_queued_two
        )

    @let
    def queue_message(self):
        return {'job_id': self.job_id, 'project_name': self.project_name}

    @let
    def queue_message_two(self):
        return {'job_id': self.job_id_two, 'project_name': self.project_name_two}

    @set_up
    def set_up(self):
        self.mock_time.return_value = self.queued_time + self.time_since_queued

    def test_has_job_id(self):
        self.assertEqual(self.job_id, self.queued_job.job_id)

    def test_has_queued_time(self):
        self.assertEqual(self.queued_time, self.queued_job.queued_time)

    def test_has_project_name(self):
        self.assertEqual(self.project_name, self.queued_job.project_name)

    def test_has_time_since_queued(self):
        self.assertEqual(
            self.time_since_queued,
            self.queued_job.time_since_queued
        )

    def test_find_async_returns_none_when_job_does_not_exist(self):
        async_job = QueuedJob.find_async(self.mock_redis_pipeline, self.job_id)
        self.mock_redis_pipeline.execute()
        self.assertIsNone(async_job.get())

    def test_find_async_returns_data_for_single_job(self):
        self._store_job_data()

        async_job = QueuedJob.find_async(self.mock_redis_pipeline, self.job_id)
        self.mock_redis_pipeline.execute()
        job = async_job.get()

        self.assertEqual(self.queued_job, job)

    def test_all_async_returns_empty_list_when_no_queued_jobs(self):
        jobs = QueuedJob.all()
        self.assertEqual([], jobs)

    def test_all_async_returns_jobs(self):
        self._store_job_data()

        jobs = QueuedJob.all()
        self.assert_list_contains_items([self.queued_job], jobs)

    def test_all_async_returns_jobs_multiple_jobs(self):
        self._store_job_data()
        self._store_job_data_two()

        jobs = QueuedJob.all()
        self.assert_list_contains_items([self.queued_job, self.queued_job_two], jobs)

    def _store_job_data(self):
        from foundations_contrib.consumers.jobs.queued.creation_time import CreationTime
        from foundations_contrib.consumers.jobs.queued.project_name import ProjectName
        from foundations_contrib.consumers.jobs.queued.global_listing import GlobalListing

        CreationTime(self.mock_redis).call(self.queue_message, self.queued_time, {})
        ProjectName(self.mock_redis).call(self.queue_message, self.queued_time, {})
        GlobalListing(self.mock_redis).call(self.queue_message, self.queued_time, {})

    def _store_job_data_two(self):
        from foundations_contrib.consumers.jobs.queued.creation_time import CreationTime
        from foundations_contrib.consumers.jobs.queued.project_name import ProjectName
        from foundations_contrib.consumers.jobs.queued.global_listing import GlobalListing

        CreationTime(self.mock_redis).call(self.queue_message_two, self.queued_time_two, {})
        ProjectName(self.mock_redis).call(self.queue_message_two, self.queued_time_two, {})
        GlobalListing(self.mock_redis).call(self.queue_message_two, self.queued_time_two, {})
