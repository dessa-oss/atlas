

from foundations_spec.extensions import let_fake_redis
from foundations_spec import *

from foundations_rest_api.v2beta.controllers.project_metrics_controller import ProjectMetricsController

class TestProjectMetricsController(Spec):

    mock_redis = let_fake_redis()
    mock_tag_set_klass = let_patch_mock_with_conditional_return('foundations_events.producers.tag_set.TagSet')
    mock_tag_set = let_mock()
    mock_message_router = let_patch_mock('foundations_contrib.global_state.message_router')

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def project_name(self):
        return self.faker.name()

    @let
    def controller(self):
        return ProjectMetricsController()

    @let
    def project_metric_logger(self):
        from foundations_events.consumers.project_metrics import ProjectMetrics
        return ProjectMetrics(self.mock_redis)

    @let
    def single_project_metric_logger(self):
        from foundations_events.consumers.single_project_metric import SingleProjectMetric
        return SingleProjectMetric(self.mock_redis)

    @set_up
    def set_up(self):
        self.patch('foundations_rest_api.global_state.redis_connection', self.mock_redis)

    @quarantine
    def test_index_returns_timestamp_ordered_metrics(self):
        self.controller.params = {'project_name': self.project_name}
        self._log_metric(33, 'job13', 'metric77', 123.4)

        expected_output = [
            {
                'metric_name': 'metric77',
                'values': [['job13', 123.4]]
            }
        ]
        self.assertEqual(expected_output, self.controller.index().as_json())

    @quarantine
    def test_index_returns_timestamp_ordered_metrics_different_metrics(self):
        self.controller.params = {'project_name': self.project_name}
        self._log_metric(321, 'job1', 'metric1', 432)
        self._log_metric(123, 'job2', 'metric1', 843)
        self._log_metric(123, 'job1', 'metric2', 221)

        expected_output = [
            {
                'metric_name': 'metric1',
                'values': [['job2', 843], ['job1', 432]]
            },
            {
                'metric_name': 'metric2',
                'values': [['job1', 221]]
            }
        ]
        self.assertEqual(expected_output, self.controller.index().as_json())

    @quarantine
    def test_index_returns_timestamp_ordered_metrics_metric_filter(self):
        metric_name = self.faker.name()
        self.controller.params = {'project_name': self.project_name, 'metric_name': metric_name}
        self._log_metric(321, 'job1', metric_name, 432)
        self._log_metric(123, 'job2', metric_name, 843)
        self._log_metric(123, 'job1', 'metric2', 221)

        expected_output = [
            {
                'metric_name': metric_name,
                'values': [['job2', 843], ['job1', 432]]
            }
        ]
        self.assertEqual(expected_output, self.controller.index().as_json())

    def _log_metric(self, timestamp, job_id, key, value):

        message = {'project_name': self.project_name, 'job_id': job_id, 'key': key, 'value': value}
        self.project_metric_logger.call(message, timestamp, None)
        self.single_project_metric_logger.call(message, timestamp, None)


