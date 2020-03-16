
import unittest
from mock import Mock

from foundations_events.consumers.jobs.completed.job_state import JobState


class TestCompletedJobState(unittest.TestCase):

    def setUp(self):
        self._redis = Mock()
        self._consumer = JobState(self._redis)

    def test_adds_job_to_project_completed_listing(self):
        self._consumer.call({'job_id': 'my fantastic job'}, None, None)
        self._redis.set.assert_called_with(
            'jobs:my fantastic job:state', 'completed')

    def test_adds_job_to_project_completed_listing_different_job(self):
        self._consumer.call({'job_id': 'my plastic stages'}, None, None)
        self._redis.set.assert_called_with(
            'jobs:my plastic stages:state', 'completed')
