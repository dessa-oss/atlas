"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from freezegun import freeze_time
from foundations.stage_logger import StageLogger


class TestStageLogger(unittest.TestCase):

    class MockClass(object):
        pass

    def setUp(self):
        from foundations.stage_context import StageContext

        self._pipeline_context = self.MockClass()
        self._stage = self.MockClass()
        self._stage_config = self.MockClass()
        self._stage_context = StageContext()
        self._logger = StageLogger(self._pipeline_context, self._stage, self._stage_config, self._stage_context)

    def test_log_metric_stores_metric(self):
        self._logger.log_metric('loss', 0.553)
        self.assertEqual({'loss': 0.553}, self._stage_log_to_dict())

    def test_log_metric_stores_metric_different_metric(self):
        self._logger.log_metric('rocauc', 0.77)
        self.assertEqual({'rocauc': 0.77}, self._stage_log_to_dict())

    def test_log_metric_stores_current_time(self):
        with freeze_time():
            from time import time

            self._logger.log_metric('rocauc', 0.77)
            self.assertDictContainsSubset({'timestamp': time()}, self._stage_context.stage_log[0])

    def test_log_metric_stores_metric_multiple_metrics(self):
        self._logger.log_metric('rocauc', 0.77)
        self._logger.log_metric('loss', 0.553)
        self.assertEqual({'rocauc': 0.77, 'loss': 0.553}, self._stage_log_to_dict())

    def test_log_metric_supports_lists(self):
        self._logger.log_metric('loss', 0.73)
        self._logger.log_metric('loss', 0.54)
        self.assertEqual({'loss': [0.73, 0.54]}, self._stage_log_to_dict())

    def test_log_metric_supports_larger_lists(self):
        self._logger.log_metric('accuracy', 0.73)
        self._logger.log_metric('accuracy', 0.75)
        self._logger.log_metric('accuracy', 0.74)
        self.assertEqual({'accuracy': [0.73, 0.75, 0.74]}, self._stage_log_to_dict())

    def test_pipeline_context(self):
        self.assertEqual(self._pipeline_context, self._logger.pipeline_context())

    def test_stage(self):
        self.assertEqual(self._stage, self._logger.stage())

    def test_stage_context(self):
        self.assertEqual(self._stage_context, self._logger.stage_context())

    def test_stage_config(self):
        self.assertEqual(self._stage_config, self._logger.stage_config())

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