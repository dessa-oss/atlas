
from foundations_spec import *
from foundations.job_metrics import log_metric
from foundations_internal.fast_serializer import deserialize

class TestLogMetric(Spec):

    class MockMessageRouter(object):
        
        def __init__(self):
            self.logged_metrics = []

        def push_message(self, name, message):
            self.logged_metrics.append({name: message})

    mock_logger = let_mock()

    @let_now
    def mock_get_logger(self):
        mock = self.patch('foundations_contrib.log_manager.LogManager.get_logger', ConditionalReturn())
        mock.return_when(self.mock_logger, 'foundations.utils')
        mock.return_when(self.mock_logger, 'foundations_events.message_router')
        return mock

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

    @set_up
    def set_up(self):
        import fakeredis
        import os
        from foundations_contrib.global_state import message_router

        foundations_job_function = self.patch('foundations_contrib.global_state.current_foundations_job')

        self.foundations_job = Mock()
        self.foundations_job.job_id = ValueError()
        self.foundations_job.is_in_running_job.return_value = False
        self.foundations_job.project_name = self.fake_project_name
        foundations_job_function.return_value = self.foundations_job

        self._redis = self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())
        self._message_router = message_router
        self._message_router.reset_routes()
        self._set_up_routes()

    def _set_up_routes(self):
        from foundations_events.consumers.job_metric_consumer import JobMetricConsumer
        from foundations_events.consumers.job_metric_name_consumer import JobMetricNameConsumer
        from foundations_events.consumers.project_metrics import ProjectMetrics
        from foundations_events.consumers.single_project_metric import SingleProjectMetric

        self._message_router.add_listener(JobMetricConsumer(self._redis), 'job_metrics')
        self._message_router.add_listener(JobMetricNameConsumer(self._redis), 'job_metrics')
        self._message_router.add_listener(ProjectMetrics(self._redis), 'job_metrics')
        self._message_router.add_listener(SingleProjectMetric(self._redis), 'job_metrics')

    def _set_job_running(self):
        self.foundations_job.job_id = self.fake_job_id
        self.foundations_job.is_in_running_job.return_value = True

    def _run_job_and_log_metric(self, metric_name, metric_value):
        self._set_job_running()
        log_metric(metric_name, metric_value)

    def _run_job_and_log_two_metrics(self):
        self._set_job_running()
        log_metric(self.fake_metric_name, self.fake_metric_value)
        log_metric(self.fake_metric_name_2, self.fake_metric_value_2)

    def _assert_expected_metrics_for_project_metrics(self, expected_metrics):
        metrics_from_redis = set()

        metric_names = [metric_name for metric_name, _ in expected_metrics]
        metric_values = [metric_value for _, metric_value in expected_metrics]

        for metric_name in metric_names:
            metric_from_redis = self._redis.hget(f'projects:{self.fake_project_name}:metrics', f'{self.fake_job_id}:{metric_name}')
            processed_metric = deserialize(metric_from_redis)[1]
            metrics_from_redis.add(processed_metric)

        self.assertEqual(set(metric_values), metrics_from_redis)

    def _assert_expected_metrics_for_single_project_metrics(self, expected_metrics):
        metrics_from_redis = set()

        metric_names = [metric_name for metric_name, _ in expected_metrics]
        metric_values = [metric_value for _, metric_value in expected_metrics]

        for metric_name in metric_names:
            metric_from_redis = self._redis.hget(f'projects:{self.fake_project_name}:metrics:{metric_name}', self.fake_job_id)
            processed_metric = deserialize(metric_from_redis)[1]
            metrics_from_redis.add(processed_metric)

        self.assertEqual(set(metric_values), metrics_from_redis)

    def test_log_metric_stores_metric_through_job_metric_consumer(self):
        self._run_job_and_log_metric(self.fake_metric_name, self.fake_metric_value)

        expected_metric = (self.fake_metric_name, self.fake_metric_value)
        metric_from_redis = self._redis.rpop(f'jobs:{self.fake_job_id}:metrics')
        actual_metric = deserialize(metric_from_redis)

        self.assertEqual(expected_metric, actual_metric[1:])

    def test_log_metric_stores_job_metric_name(self):
        self._run_job_and_log_metric(self.fake_metric_name, self.fake_metric_value)

        metric_name_from_redis = self._redis.smembers(f'project:{self.fake_project_name}:metrics')
        actual_metric_name = {metric.decode() for metric in metric_name_from_redis}

        self.assertEqual({self.fake_metric_name}, actual_metric_name)

    def test_log_metric_stores_project_metric(self):
        self._run_job_and_log_metric(self.fake_metric_name, self.fake_metric_value)
        self._assert_expected_metrics_for_project_metrics([(self.fake_metric_name, self.fake_metric_value)])

    def test_log_metric_stores_single_project_metric(self):
        self._run_job_and_log_metric(self.fake_metric_name, self.fake_metric_value)
        self._assert_expected_metrics_for_single_project_metrics([(self.fake_metric_name, self.fake_metric_value)])

    def test_log_metric_can_log_multiple_messages_through_job_metric_consumer(self):
        self._run_job_and_log_two_metrics()

        metrics_from_redis = self._redis.lrange(f'jobs:{self.fake_job_id}:metrics', 0, 2)
        metrics = [deserialize(metric) for metric in metrics_from_redis]
        metric_values = set([metric[1:] for metric in metrics])

        expected_metrics = set([(self.fake_metric_name, self.fake_metric_value), (self.fake_metric_name_2, self.fake_metric_value_2)])

        self.assertEqual(expected_metrics, metric_values)
    
    def test_log_metric_can_log_multiple_metric_names_through_job_metric_name_consumer(self):
        self._run_job_and_log_two_metrics()

        metric_names_from_redis = self._redis.smembers(f'project:{self.fake_project_name}:metrics')
        actual_metric_names = {metric.decode() for metric in metric_names_from_redis}

        self.assertEqual({self.fake_metric_name, self.fake_metric_name_2}, actual_metric_names)

    def test_log_metric_can_store_multiple_project_metrics(self):
        self._run_job_and_log_two_metrics()
        self._assert_expected_metrics_for_project_metrics([(self.fake_metric_name, self.fake_metric_value), (self.fake_metric_name_2, self.fake_metric_value_2)])

    def test_log_metric_can_store_multiple_single_project_metrics(self):
        self._run_job_and_log_two_metrics()
        self._assert_expected_metrics_for_single_project_metrics([(self.fake_metric_name, self.fake_metric_value), (self.fake_metric_name_2, self.fake_metric_value_2)])

    def test_log_metric_stores_singleton_list_metric_through_job_metric_consumer(self):
        self._run_job_and_log_metric('loss', [2])

        expected_metric = ('loss', 2)
        metric_from_redis = self._redis.rpop(f'jobs:{self.fake_job_id}:metrics')
        actual_metric = deserialize(metric_from_redis)

        self.assertEqual(expected_metric, actual_metric[1:])

    def test_log_metric_stores_singleton_list_project_metric(self):
        self._run_job_and_log_metric('loss', [2])
        self._assert_expected_metrics_for_project_metrics([('loss', 2)])

    def test_log_metric_stores_singleton_list_single_project_metric(self):
        self._run_job_and_log_metric('loss', [2])
        self._assert_expected_metrics_for_single_project_metrics([('loss', 2)])

    def test_log_metric_logs_key_invalid_key_type(self):
        with self.assertRaises(ValueError) as error_context:
            log_metric(5, 0.554)

        self.assertIn('Invalid metric name `5`', error_context.exception.args)

    def test_log_metric_logs_key_invalid_key_type_different_key(self):
        with self.assertRaises(ValueError) as error_context:
            log_metric(5.44, 0.554)

        self.assertIn('Invalid metric name `5.44`',
                      error_context.exception.args)

    def test_log_metric_stores_list_metric_through_job_metric_consumer(self):
        self._run_job_and_log_metric('loss', ["this", "that", "the other"])

        expected_metrics = {
            ('loss', 'this'),
            ('loss', 'that'),
            ('loss', 'the other')
        }

        metrics_from_redis = self._redis.lrange(f'jobs:{self.fake_job_id}:metrics', 0, 4)
        metrics = [deserialize(metric) for metric in metrics_from_redis]
        metric_values = set([metric[1:] for metric in metrics])

        self.assertEqual(expected_metrics, metric_values)

    def test_log_metric_on_list_stores_one_job_metric_name(self):
        self._run_job_and_log_metric('loss', ["this", "that", "the other"])

        metric_name_from_redis = self._redis.smembers(f'project:{self.fake_project_name}:metrics')
        actual_metric_name = {metric.decode() for metric in metric_name_from_redis}

        self.assertEqual({'loss'}, actual_metric_name)

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

    def _logged_metrics(self):
        return self._message_router.logged_metrics
