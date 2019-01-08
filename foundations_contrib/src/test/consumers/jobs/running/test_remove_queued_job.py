"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_contrib.consumers.jobs.running.remove_queued_job import RemoveQueuedJob


class TestRemoveQueuedJob(unittest.TestCase):

    def setUp(self):
        self._redis = Mock()
        self._consumer = RemoveQueuedJob(self._redis)

    def test_call_removes_job_from_project_queued(self):
        self._consumer.call({'project_name': 'here be dragons', 'job_id': 'dragons'}, None, None)
        self._redis.srem.assert_called_with('project:here be dragons:jobs:queued', 'dragons')

    def test_call_removes_job_from_project_queued_different_job_id(self):
        self._consumer.call({'project_name': 'here be dragons', 'job_id': 'wyverns'}, None, None)
        self._redis.srem.assert_called_with('project:here be dragons:jobs:queued', 'wyverns')

    def test_call_removes_job_from_project_queued_different_project_name(self):
        self._consumer.call({'project_name': 'here be no dragons', 'job_id': 'dragons'}, None, None)
        self._redis.srem.assert_called_with('project:here be no dragons:jobs:queued', 'dragons')
