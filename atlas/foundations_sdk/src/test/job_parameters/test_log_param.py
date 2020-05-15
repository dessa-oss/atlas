
from foundations_spec import *

from foundations.job_parameters import log_param

class TestLogParam(Spec):

    mock_logger = let_mock()

    @let_now
    def mock_get_logger(self):
        mock = self.patch('foundations_contrib.log_manager.LogManager.get_logger', ConditionalReturn())
        mock.return_when(self.mock_logger, 'foundations.utils')
        return mock

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def fake_key(self):
        return self.faker.word()

    @let
    def fake_key_two(self):
        return self.faker.word()

    def fake_literal(self):
        case_selector = self.faker.random.random()

        if case_selector < 0.33:
            return self.faker.word()
        elif case_selector < 0.66:
            return self.faker.random_int(0, 100000)
        else:
            return self.faker.random.random()

    @let
    def fake_value(self):
        return self.fake_literal()

    @let
    def fake_value_two(self):
        return self.fake_literal()

    @set_up
    def set_up(self):
        import fakeredis

        foundations_job_function = self.patch('foundations_contrib.global_state.current_foundations_job')

        self.foundations_job = Mock()
        self.foundations_job.job_id = ValueError()
        self.foundations_job.is_in_running_job.return_value = False
        self.foundations_job.project_name.return_value = 'default'
        foundations_job_function.return_value = self.foundations_job

        self.redis_connection = self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    def test_log_param_inserts_parameter_key_into_input_params_keys_set(self):
        self.foundations_job.project_name = self.project_name
        self._set_job_running()
        
        log_param(self.fake_key, self.fake_value)
        self.assertEqual(set([bytes(self.fake_key, 'ascii')]), self.redis_connection.smembers('projects:{}:{}'.format(self.project_name, 'input_parameter_names')))

    def test_log_param_sets_input_parameter_data(self):
        from foundations_internal.foundations_serializer import loads

        self.foundations_job.project_name = self.project_name
        self._set_job_running()
        
        log_param(self.fake_key, self.fake_value)
        expected_params = [{'argument': {'name': self.fake_key, 'value': {'type': 'dynamic', 'name': self.fake_key}}, 'stage_uuid': 'stageless'}]
        actual_params = loads(self.redis_connection.get('jobs:{}:{}'.format(self.job_id, 'input_parameters')))
        self.assertEqual(expected_params, actual_params)

    def test_log_param_sets_input_parameter_data_with_multiple_params(self):
        from foundations_internal.foundations_serializer import loads

        self.foundations_job.project_name = self.project_name
        self._set_job_running()
        
        log_param(self.fake_key, self.fake_value)
        log_param(self.fake_key_two, self.fake_value_two)
        expected_params = [
            {'argument': {'name': self.fake_key, 'value': {'type': 'dynamic', 'name': self.fake_key}}, 'stage_uuid': 'stageless'},
            {'argument': {'name': self.fake_key_two, 'value': {'type': 'dynamic', 'name': self.fake_key_two}}, 'stage_uuid': 'stageless'}
        ]

        actual_params = loads(self.redis_connection.get('jobs:{}:{}'.format(self.job_id, 'input_parameters')))
        self.assertEqual(expected_params, actual_params)

    def test_log_param_inserts_parameter_key_into_projects_params_keys_set(self):
        self.foundations_job.project_name = self.project_name
        self._set_job_running()
        
        log_param(self.fake_key, self.fake_value)
        self.assertEqual(set([bytes(self.fake_key, 'ascii')]), self.redis_connection.smembers('projects:{}:{}'.format(self.project_name, 'job_parameter_names')))

    def test_log_param_sets_job_run_data(self):
        import json

        self.foundations_job.project_name = self.project_name
        self._set_job_running()
        
        log_param(self.fake_key, self.fake_value)
        expected_params = {self.fake_key: self.fake_value}
        actual_params = json.loads(self.redis_connection.get('jobs:{}:{}'.format(self.job_id, 'parameters')))
        self.assertEqual(expected_params, actual_params)

    def test_log_param_sets_job_run_data_with_multiple_params(self):
        import json

        self.foundations_job.project_name = self.project_name
        self._set_job_running()
        
        log_param(self.fake_key, self.fake_value)
        log_param(self.fake_key_two, self.fake_value_two)
        expected_params = {
            self.fake_key: self.fake_value,
            self.fake_key_two: self.fake_value_two
        }

        actual_params = json.loads(self.redis_connection.get('jobs:{}:{}'.format(self.job_id, 'parameters')))
        self.assertEqual(expected_params, actual_params)

    def _set_job_running(self):
        self.foundations_job.job_id = self.job_id
        self.foundations_job.is_in_running_job.return_value = True