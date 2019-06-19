"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_contrib.global_metric_logger import GlobalMetricLogger

class TestGlobalMetricLogger(Spec):

    mock_get_logger = let_patch_mock('foundations_contrib.global_state.log_manager.get_logger', ConditionalReturn())
    mock_logger = let_mock()

    class MockClass(object):
        pass

    @let
    def fake_metric_name(self):
        return self.faker.word()

    @let
    def fake_metric_value(self):
        return self.faker.random.random()

    @let
    def fake_job_id(self):
        return self.faker.uuid4()

    def setUp(self):
        from foundations_internal.stage_context import StageContext
        from foundations.global_state import current_foundations_context

        current_context = current_foundations_context()
        self._pipeline_context = current_context.pipeline_context()
        self._stage_context = self._pipeline_context.global_stage_context

        self._logger = GlobalMetricLogger(self._pipeline_context, self._stage_context)
        self.mock_get_logger.return_when(self.mock_logger, 'foundations_contrib.global_metric_logger')
        self._pipeline_context.file_name = None
        self._stage_context.stage_log = []

    def test_log_metric_stores_metric(self):
        self._pipeline_context.file_name = self.fake_job_id
        self._logger.log_metric(self.fake_metric_name, self.fake_metric_value)
        self.assertEqual({self.fake_metric_name: self.fake_metric_value}, self._stage_log_to_dict())

    # def test_log_metric_does_nothing_if_not_in_job(self):
    #     self._logger.log_metric(self.fake_metric_name, self.fake_metric_value)
    #     self.assertEqual({}, self._stage_log_to_dict())

    def test_log_metric_shows_warning_if_not_in_running_job(self):
        self._logger.log_metric(self.fake_metric_name, self.fake_metric_value)
        self.mock_logger.warning.assert_called_with('Cannot log metric if not deployed with foundations deploy')

    def _stage_log_to_dict(self):
        log = {}

        for log_item in self._stage_context.stage_log:
            key = log_item['key']
            value = log_item['value']
            if key in log:
                previous_value = log[key]
                if isinstance(previous_value, list):
                    log[key].append(value)
                else:
                    log[key] = [previous_value, value]
            else:
                log[key] = value

        return log