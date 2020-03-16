
import unittest
from mock import Mock

from foundations_events.consumers.jobs.queued.project_tracker import ProjectTracker

class TestProjectTracker(unittest.TestCase):
    
    def setUp(self):
        self._redis = Mock()
        self._consumer = ProjectTracker(self._redis)
        self._redis.zscore.return_value = None

    def test_call_saves_project_name_and_timestamp(self):
        self._consumer.call({'project_name': 'cats and aliens'}, 323424.33, None)
        self._redis.execute_command.assert_called_with('ZADD', 'projects', 'NX', 323424.33, 'cats and aliens')

    def test_call_saves_project_name_and_timestamp_different_timestamp(self):
        self._consumer.call({'project_name': 'cats and aliens'}, 24.33, None)
        self._redis.execute_command.assert_called_with('ZADD', 'projects', 'NX', 24.33, 'cats and aliens')

    def test_call_saves_project_name_and_timestamp_different_project(self):
        self._consumer.call({'project_name': 'potato farm'}, 24.33, None)
        self._redis.execute_command.assert_called_with('ZADD', 'projects', 'NX', 24.33, 'potato farm')
