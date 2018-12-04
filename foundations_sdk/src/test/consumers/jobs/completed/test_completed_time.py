"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations.consumers.jobs.completed.completed_time import CompletedTime

class TestCompletedTime(unittest.TestCase):
    
    def setUp(self):
        self._redis = Mock()
        self._consumer = CompletedTime(self._redis)

    def test_call_saves_completed_time(self):
        self._consumer.call({'job_id': 'space pinball'}, 34344, None)
        self._redis.set.assert_called_with('jobs:space pinball:completed_time', '34344')

    def test_call_saves_completed_time_different_job_id(self):
        self._consumer.call({'job_id': 'dimensional pinball'}, 34344, None)
        self._redis.set.assert_called_with('jobs:dimensional pinball:completed_time', '34344')

    def test_call_saves_completed_time_different_time(self):
        self._consumer.call({'job_id': 'space pinball'}, 99999, None)
        self._redis.set.assert_called_with('jobs:space pinball:completed_time', '99999')