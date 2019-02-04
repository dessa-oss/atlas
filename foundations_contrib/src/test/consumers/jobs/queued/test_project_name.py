"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_contrib.consumers.jobs.queued.project_name import ProjectName


class TestProjectName(unittest.TestCase):

    def setUp(self):
        self._redis = Mock()
        self._consumer = ProjectName(self._redis)

    def test_adds_job_to_project_queued_listing(self):
        self._consumer.call({'project_name': 'my fantastic project', 'job_id': 'my fantastic job'}, None, None)
        self._redis.set.assert_called_with('jobs:my fantastic job:project', 'my fantastic project')

    def test_adds_job_to_project_queued_listing_different_project(self):
        self._consumer.call({'project_name': 'my stupendous project', 'job_id': 'my fantastic job'}, None, None)
        self._redis.set.assert_called_with('jobs:my fantastic job:project', 'my stupendous project')

    def test_adds_job_to_project_queued_listing_different_job(self):
        self._consumer.call({'project_name': 'my fantastic project', 'job_id': 'my stupendous job'}, None, None)
        self._redis.set.assert_called_with('jobs:my stupendous job:project', 'my fantastic project')
