"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_contrib.models.queued_job_query import QueuedJobQuery

from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let

class TestQueuedJobQuery(Spec):
    
    @let
    def mock_redis(self):
        from fakeredis import FakeRedis
        return FakeRedis()

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
    def query(self):
        return QueuedJobQuery(self.mock_redis, self.job_id)

    @let
    def queue_message(self):
        return {'job_id': self.job_id, 'project_name': self.project_name}

    def test_returns_queued_time(self):
        from foundations_contrib.consumers.jobs.queued.creation_time import CreationTime

        CreationTime(self.mock_redis).call(self.queue_message, self.queued_time, {})
        self.assertEqual(self.queued_time, float(self.query.queued_time()))

    def test_returns_project_name(self):
        from foundations_contrib.consumers.jobs.queued.project_name import ProjectName

        ProjectName(self.mock_redis).call(self.queue_message, self.queued_time, {})
        self.assertEqual(self.project_name, self.query.project_name().decode())

    def test_exists_returns_false_when_not_queued(self):
        self.assertFalse(self.query.exists())

    def test_exists_returns_true_when_queued(self):
        from foundations_contrib.consumers.jobs.queued.global_listing import GlobalListing

        GlobalListing(self.mock_redis).call(self.queue_message, self.queued_time, {})
        self.assertTrue(self.query.exists())
