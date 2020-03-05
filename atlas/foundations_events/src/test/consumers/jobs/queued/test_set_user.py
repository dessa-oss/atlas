
import unittest
from mock import Mock

from foundations_events.consumers.jobs.queued.set_user import SetUser


class TestSetUser(unittest.TestCase):

    def setUp(self):
        self._redis = Mock()
        self._consumer = SetUser(self._redis)

    def test_call_sets_jobs_user(self):
        self._consumer.call({'job_id': 'my fantastic job','user_name': 'pippinstall'}, None, None)
        self._redis.set.assert_called_with('jobs:my fantastic job:user', 'pippinstall')

    def test_call_sets_jobs_user_different_user(self):
        self._consumer.call({'job_id': 'my plastic stages','user_name': 'cookiemonster'}, None, None)
        self._redis.set.assert_called_with('jobs:my plastic stages:user', 'cookiemonster')
