"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, patch, call

from foundations.middleware.metric_log_middleware import MetricLogMiddleware
from foundations.global_state import message_router
from uuid import uuid4


class TestMetricLogMiddleware(unittest.TestCase):

    def setUp(self):
        from foundations.pipeline_context import PipelineContext
        from foundations.stage_config import StageConfig
        from foundations.stage_context import StageContext
        from foundations.stage import Stage

        self._pipeline_context = PipelineContext()
        self._stage_config = StageConfig()
        self._stage_context = StageContext()
        self._uuid = str(uuid4())
        self._stage = Stage(None, self._uuid, self._function, self._function)

        self._mock_stage_cache = None
        self._called_callback = False
        self._callback_args = None
        self._callback_kwargs = None

    @patch.object(message_router, 'push_message')
    def test_call_pushes_message_one_metric_and_returns_callback_value(self, mock):
        def method(*args, **kwargs):
            return 1

        metric_1 = {'key': 'key1', 'value': 'value1', 'timestamp': 123}
        self._stage_context.stage_log.append(metric_1)

        job_id = self._make_uuid()
        self._pipeline_context.file_name = job_id

        middleware = self._make_middleware()

        self.assertEqual(middleware.call(None, None, None, (), {}, method), 1)
        mock.assert_called_with(
            'job_metrics', {'project_name': 'default', 'job_id': job_id, 'key': 'key1', 'value': 'value1'})

    @patch.object(message_router, 'push_message')
    def test_call_pushes_multiple_metrics(self, mock):
        def method(*args, **kwargs):
            pass

        metric_1 = {'key': 'carrot', 'value': 'stick', 'timestamp': 123}
        metric_2 = {'key': 'hot', 'value': 'cold', 'timestamp': 1238129}
        self._stage_context.stage_log.append(metric_1)
        self._stage_context.stage_log.append(metric_2)

        job_id = self._make_uuid()
        self._pipeline_context.file_name = job_id

        middleware = self._make_middleware()
        middleware.call(None, None, None, (), {}, method)

        call_1 = call('job_metrics', {'project_name': 'default', 'job_id': job_id,
                                      'key': 'carrot', 'value': 'stick'})
        call_2 = call('job_metrics', {'project_name': 'default', 'job_id': job_id,
                                      'key': 'hot', 'value': 'cold'})

        mock.assert_has_calls([call_1, call_2])

    def _make_uuid(self):
        from uuid import uuid4
        return str(uuid4())

    def _function(self):
        pass

    def _make_middleware(self):
        return MetricLogMiddleware(self._pipeline_context, self._stage_config,
                                   self._stage_context, self._stage)
