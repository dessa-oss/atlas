"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_contrib.global_metric_logger import GlobalMetricLogger

class TestGlobalMetricLogger(Spec):

    mock_log_manager = let_patch_mock('foundations_contrib.global_state.log_manager')

    class MockMessageRouter(object):
        
        def __init__(self):
            self.logged_metrics = []

        def push_message(self, name, message):
            self.logged_metrics.append({name: message})

    @let
    def fake_metric_name(self):
        return self.faker.word()

    @let
    def fake_metric_value(self):
        return self.faker.random.random()

    @let
    def fake_job_id(self):
        return self.faker.uuid4()

    @let
    def fake_project_name(self):
        return self.faker.word()

    @let
    def message(self):
        return {
            'project_name': self.fake_project_name, 
            'job_id': self.fake_job_id, 
            'key': self.fake_metric_name, 
            'value': self.fake_metric_value
        }

    @let
    def fake_metric_name_2(self):
        return self.faker.word()

    @let
    def fake_metric_value_2(self):
        return self.faker.random.random()

    @let
    def message_2(self):
        return {
            'project_name': self.fake_project_name, 
            'job_id': self.fake_job_id, 
            'key': self.fake_metric_name_2, 
            'value': self.fake_metric_value_2
        }

    def setUp(self):
        from foundations_internal.pipeline_context import PipelineContext

        self._pipeline_context = PipelineContext()

        self._message_router = self.MockMessageRouter()
        self._logger = GlobalMetricLogger(self._message_router, self._pipeline_context)

        self.mock_logger = Mock()
        self.mock_get_logger = ConditionalReturn()
        self.mock_get_logger.return_when(self.mock_logger, 'foundations_contrib.global_metric_logger')
        self.mock_log_manager.get_logger = self.mock_get_logger

        self._pipeline_context.file_name = None
        self._pipeline_context.provenance.project_name = self.fake_project_name

    def test_log_metric_stores_metric(self):
        self._pipeline_context.file_name = self.fake_job_id
        self._logger.log_metric(self.fake_metric_name, self.fake_metric_value)
        self.assertEqual([{'job_metrics': self.message}], self._logged_metrics())

    def test_log_metric_shows_warning_if_not_in_running_job(self):
        self._pipeline_context.file_name = None
        self._logger.log_metric(self.fake_metric_name, self.fake_metric_value)
        self.mock_logger.warning.assert_called_with('Cannot log metric if not deployed with foundations deploy')

    def test_log_metric_does_not_show_warning_if_in_running_job(self):
        self._pipeline_context.file_name = self.fake_job_id
        self._logger.log_metric(self.fake_metric_name, self.fake_metric_value)
        self.mock_logger.warning.assert_not_called()

    def test_log_metric_can_log_multiple_messages(self):
        self._pipeline_context.file_name = self.fake_job_id
        self._logger.log_metric(self.fake_metric_name, self.fake_metric_value)
        self._logger.log_metric(self.fake_metric_name_2, self.fake_metric_value_2)
        self.assertEqual([{'job_metrics': self.message}, {'job_metrics': self.message_2}], self._logged_metrics())

    def test_log_metric_does_not_log_anything_if_not_in_running_job(self):
        self._pipeline_context.file_name = None
        self._logger.log_metric(self.fake_metric_name, self.fake_metric_value)
        self.assertEqual([], self._logged_metrics())

    def _logged_metrics(self):
        return self._message_router.logged_metrics