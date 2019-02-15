"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_internal.testing.helpers import let, let_patch_mock
from foundations_internal.testing.helpers.spec import Spec

from foundations_contrib.models.queued_job import QueuedJob

class TestQueuedJob(Spec):

    mock_redis = let_patch_mock('foundations.global_state.redis_connection')

    @let
    def faker(self):
        import faker
        return faker.Faker()

    @let
    def job_id(self):
        return self.faker.sha256()
    
    @let
    def queued_time(self):
        import time
        return time.time()
    
    @let
    def project_name(self):
        import uuid
        return str(uuid.uuid4())

    @let
    def time_since_queued(self):
        import time
        return time.time()

    @let
    def queued_job(self):
        return QueuedJob(job_id=self.job_id, queued_time=self.queued_time, project_name=self.project_name, time_since_queued=self.time_since_queued)

    def test_has_job_id(self):
        self.assertEqual(self.job_id, self.queued_job.job_id)

    def test_has_queued_time(self):
        self.assertEqual(self.queued_time, self.queued_job.queued_time)

    def test_has_project_name(self):
        self.assertEqual(self.project_name, self.queued_job.project_name)

    def test_has_time_since_queued(self):
        self.assertEqual(self.time_since_queued, self.queued_job.time_since_queued)
