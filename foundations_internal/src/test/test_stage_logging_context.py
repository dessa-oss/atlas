"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_internal.stage_logging_context import StageLoggingContext


class TestStageLoggingContext(unittest.TestCase):

    class MockLogger(object):

        def __init__(self):
            self.key = None
            self.value = None

        def log_metric(self, key, value):
            self.key = key
            self.value = value

    def setUp(self):
        self._logger = self.MockLogger()
        self._context = StageLoggingContext(self._logger)

    def test_log_metric_logs_key(self):
        self._context.log_metric('loss', 0.554)
        self.assertEqual('loss', self._logger.key)

    def test_log_metric_logs_key_different_key(self):
        self._context.log_metric('accuracy', 0.554)
        self.assertEqual('accuracy', self._logger.key)

    def test_log_metric_logs_key_invalid_key_type(self):
        with self.assertRaises(ValueError) as error_context:
            self._context.log_metric(5, 0.554)

        self.assertIn('Invalid metric name `5`', error_context.exception.args)

    def test_log_metric_logs_key_invalid_key_type_different_key(self):
        with self.assertRaises(ValueError) as error_context:
            self._context.log_metric(5.44, 0.554)

        self.assertIn('Invalid metric name `5.44`',
                      error_context.exception.args)

    def test_log_metric_logs_value(self):
        self._context.log_metric('loss', 0.554)
        self.assertEqual(0.554, self._logger.value)

    def test_log_metric_value_raises_exception_not_number_or_string(self):
        expected_error_message = 'Invalid metric with key="loss" of value=[2] with type <class \'list\'>. Value should be of type string or number'

        with self.assertRaises(TypeError) as metric:
            self._context.log_metric('loss', [2])
        self.assertEqual(str(metric.exception), expected_error_message)

    def test_log_metric_value_raises_exception_not_number_or_string_with_different_key(self):
        expected_error_message = 'Invalid metric with key="gain" of value=[2] with type <class \'list\'>. Value should be of type string or number'

        with self.assertRaises(TypeError) as metric:
            self._context.log_metric('gain', [2])
        self.assertEqual(str(metric.exception), expected_error_message)

    def test_log_metric_value_raises_exception_not_number_or_string_different_value(self):
        expected_error_message = 'Invalid metric with key="loss" of value={\'a\': 22} with type <class \'dict\'>. Value should be of type string or number'

        with self.assertRaises(TypeError) as metric:
            self._context.log_metric('loss', {"a": 22})
        self.assertEqual(str(metric.exception), expected_error_message)

    def test_log_metric_value_raises_exception_cut_down_to_thirty_chars(self):
        metric_value = [[1] * 50]

        expected_error_message = 'Invalid metric with key="loss" of value=[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ... with type <class \'list\'>. Value should be of type string or number'

        with self.assertRaises(TypeError) as metric:
            self._context.log_metric('loss', metric_value)
        self.assertEqual(str(metric.exception), expected_error_message)

    def test_log_metric_value_raises_exception_not_number_or_string_custom_class_using_default_repr(self):
        class MyCoolClass(object):
            def __init__(self):
                pass

        metric_value = MyCoolClass()
        representation = str(metric_value)[:30] + " ..."
        expected_error_message_format = 'Invalid metric with key="loss" of value={} with type {}. Value should be of type string or number'
        expected_error_message = expected_error_message_format.format(representation, type(metric_value))

        with self.assertRaises(TypeError) as metric:
            self._context.log_metric('loss', metric_value)
        self.assertEqual(str(metric.exception), expected_error_message)

    def test_log_metric_logs_value_different_value(self):
        self._context.log_metric('loss', 0.1554)
        self.assertEqual(0.1554, self._logger.value)

    def test_change_logger_changes_logger(self):
        logger_two = self.MockLogger()

        with self._context.change_logger(logger_two):
            self._context.log_metric('loss', 0.1554)
            self.assertEqual(0.1554, logger_two.value)

    def test_change_logger_resets_logger(self):
        logger_two = self.MockLogger()

        with self._context.change_logger(logger_two):
            pass

        self._context.log_metric('loss', 0.1554)
        self.assertEqual(0.1554, self._logger.value)
