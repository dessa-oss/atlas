"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations.job_metrics import log_metric

@skip
class TestLogMetric(Spec):

    class MockMessageRouter(object):
        
        def __init__(self):
            self.logged_metrics = []

        def push_message(self, name, message):
            self.logged_metrics.append({name: message})

    mock_current_foundations_context = let_patch_instance('foundations_contrib.global_state.current_foundations_context')
    mock_logger = let_mock()

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

    @let_now
    def mock_get_logger(self):
        mock = self.patch('foundations_contrib.log_manager.LogManager.get_logger', ConditionalReturn())
        mock.return_when(self.mock_logger, 'foundations.job_metrics')
        mock.return_when(self.mock_logger, 'foundations_events.message_router')
        return mock

    @set_up
    def set_up(self):
        from foundations_internal.pipeline_context import PipelineContext

        self._pipeline_context = PipelineContext()
        self.mock_current_foundations_context.pipeline_context.return_value = self._pipeline_context

        self._message_router = self.MockMessageRouter()
        self.mock_message_router = self.patch('foundations_contrib.global_state.message_router', self._message_router)

        self._pipeline_context.file_name = None
        self._pipeline_context.provenance.project_name = self.fake_project_name

    @tear_down
    def tear_down(self):
        from foundations_contrib.global_state import log_manager
        log_manager.set_foundations_not_running_warning_printed(False)

    def test_log_metric_stores_metric(self):
        self._pipeline_context.file_name = self.fake_job_id
        log_metric(self.fake_metric_name, self.fake_metric_value)
        self.assertEqual([{'job_metrics': self.message}], self._logged_metrics())

    def test_log_metric_shows_warning_if_not_in_running_job(self):
        self._pipeline_context.file_name = None
        log_metric(self.fake_metric_name, self.fake_metric_value)
        self.mock_logger.warning.assert_called_with('Script not run with Foundations.')

    def test_log_metric_shows_warning_only_once_if_not_in_running_job(self):
        self._pipeline_context.file_name = None
        log_metric(self.fake_metric_name, self.fake_metric_value)
        log_metric(self.fake_metric_name, self.fake_metric_value)
        self.mock_logger.warning.assert_called_once_with('Script not run with Foundations.')

    def test_log_metric_does_not_show_warning_if_in_running_job(self):
        self._pipeline_context.file_name = self.fake_job_id
        log_metric(self.fake_metric_name, self.fake_metric_value)
        self.mock_logger.warning.assert_not_called()

    def test_log_metric_can_log_multiple_messages(self):
        self._pipeline_context.file_name = self.fake_job_id
        log_metric(self.fake_metric_name, self.fake_metric_value)
        log_metric(self.fake_metric_name_2, self.fake_metric_value_2)
        self.assertEqual([{'job_metrics': self.message}, {'job_metrics': self.message_2}], self._logged_metrics())

    def test_log_metric_does_not_log_anything_if_not_in_running_job(self):
        self._pipeline_context.file_name = None
        log_metric(self.fake_metric_name, self.fake_metric_value)
        self.assertEqual([], self._logged_metrics())
    
    def test_log_metric_logs_key_invalid_key_type(self):
        with self.assertRaises(ValueError) as error_context:
            log_metric(5, 0.554)

        self.assertIn('Invalid metric name `5`', error_context.exception.args)

    def test_log_metric_logs_key_invalid_key_type_different_key(self):
        with self.assertRaises(ValueError) as error_context:
            log_metric(5.44, 0.554)

        self.assertIn('Invalid metric name `5.44`',
                      error_context.exception.args)

    def test_log_metric_with_singleton_list(self):
        self._pipeline_context.file_name = self.fake_job_id
        log_metric('loss', [2])
        self.assertEqual([{'job_metrics': self._get_message('loss', 2)}], self._logged_metrics())

    def test_log_metric_with_another_list(self):
        self._pipeline_context.file_name = self.fake_job_id
        log_metric('loss', ["this", "that", "the other"])

        self.assertEqual([
            {'job_metrics': self._get_message('loss', 'this')},
            {'job_metrics': self._get_message('loss', 'that')},
            {'job_metrics': self._get_message('loss', 'the other')}], self._logged_metrics())

    def test_log_metric_with_invalid_list(self):
        expected_error_message = 'Invalid metric with key="bloop" of value=[<class \'Exception\'>] with type ' \
                                 '<class \'list\'>. Value should be of type string or number, or a list of ' \
                                 'strings / numbers'

        with self.assertRaises(TypeError) as metric:
            log_metric('bloop', [Exception])
        self.assertEqual(str(metric.exception), expected_error_message)

    def test_log_metric_value_raises_exception_not_number_or_string_with_different_key(self):
        expected_error_message = 'Invalid metric with key="gain" of value=[[2]] with type <class \'list\'>. ' \
                                 'Value should be of type string or number, or a list of strings / numbers'

        with self.assertRaises(TypeError) as metric:
            log_metric('gain', [[2]])
        self.assertEqual(str(metric.exception), expected_error_message)

    def test_log_metric_value_raises_exception_not_number_or_string_different_value(self):
        expected_error_message = 'Invalid metric with key="loss" of value={\'a\': 22} with type <class \'dict\'>. ' \
                                 'Value should be of type string or number, or a list of strings / numbers'

        with self.assertRaises(TypeError) as metric:
            log_metric('loss', {"a": 22})
        self.assertEqual(str(metric.exception), expected_error_message)

    def test_log_metric_value_raises_exception_cut_down_to_thirty_chars(self):
        metric_value = [[1] * 50]

        expected_error_message = 'Invalid metric with key="loss" of value=[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ... with type ' \
                                 '<class \'list\'>. Value should be of type string or number, or a list of ' \
                                 'strings / numbers'

        with self.assertRaises(TypeError) as metric:
            log_metric('loss', metric_value)
        self.assertEqual(str(metric.exception), expected_error_message)

    def test_log_metric_value_raises_exception_not_number_or_string_custom_class_using_default_repr(self):
        class MyCoolClass(object):
            def __init__(self):
                pass

        metric_value = MyCoolClass()
        representation = str(metric_value)[:30] + " ..."
        expected_error_message_format = 'Invalid metric with key="loss" of value={} with type {}. Value should be of ' \
                                        'type string or number, or a list of strings / numbers'
        expected_error_message = expected_error_message_format.format(representation, type(metric_value))

        with self.assertRaises(TypeError) as metric:
            log_metric('loss', metric_value)
        self.assertEqual(str(metric.exception), expected_error_message)

    def test_log_metric_logs_value_different_value(self):
        self._pipeline_context.file_name = self.fake_job_id
        log_metric('loss', 0.1554)
        self.assertEqual([{'job_metrics': self._get_message('loss', 0.1554)}], self._logged_metrics())

    def _get_message(self, key, value):
        return {
            'project_name': self.fake_project_name, 
            'job_id': self.fake_job_id, 
            'key': key, 
            'value': value
        }

    def _logged_metrics(self):
        return self._message_router.logged_metrics
