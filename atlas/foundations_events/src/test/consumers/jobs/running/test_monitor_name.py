
from foundations_spec import *

class TestMonitorName(Spec):

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def monitor_name(self):
        return self.faker.word()

    @let
    def project_name(self):
        return self.faker.word()
    
    @set_up
    def set_up(self):
        from foundations_events.consumers.jobs.running.monitor_name import MonitorName
        self._redis = Mock()
        self._consumer = MonitorName(self._redis)

    def test_adds_monitor_name_to_project(self):
        self._consumer.call({'project_name': self.project_name, 'monitor_name': self.monitor_name, 'job_id': self.job_id}, None, None)
        self._redis.sadd.assert_called_with(
            f'projects:{self.project_name}:monitors:{self.monitor_name}:jobs', self.job_id)