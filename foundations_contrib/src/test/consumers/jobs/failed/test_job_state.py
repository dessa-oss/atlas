"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_contrib.consumers.jobs.failed.job_state import JobState


class TestFailedJobState(unittest.TestCase):

    def setUp(self):
        self._redis = Mock()
        self._consumer = JobState(self._redis)

    def test_adds_job_to_project_failed_listing(self):
        self._consumer.call({'job_id': 'my fantastic job'}, None, None)
        self._redis.set.assert_called_with(
            'jobs:my fantastic job:state', 'Error')

    def test_adds_job_to_project_failed_listing_different_job(self):
        self._consumer.call({'job_id': 'my plastic stages'}, None, None)
        self._redis.set.assert_called_with(
            'jobs:my plastic stages:state', 'Error')
