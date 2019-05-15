"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_production.serving.package_runner import run_model_package

class TestPackageRunner(Spec):

    @let
    def fake_data(self):
        return self.faker.word()
    
    @let
    def prediction(self):
        return self.faker.word()
    
    @let
    def fake_data_that_errors(self):
        return self.faker.word()
    
    @let
    def model_package_id(self):
        return self.faker.uuid4()
    
    @let
    def number_of_calls(self):
        return self.faker.random_int(2,10)

    @let
    def communicator(self):
        from foundations_production.serving.communicator import Communicator
        return Communicator()
    
    @let
    def workspace_directory(self):
        return '/tmp/foundations_workspaces/{}'.format(self.model_package_id)

    mock_create_job_workspace = let_patch_mock('foundations_production.serving.create_job_workspace')
    mock_chdir = let_patch_mock('os.chdir')
    mock_predictor = let_mock()

    mock_foundations_context = let_patch_instance('foundations_contrib.global_state.current_foundations_context')
    mock_pipeline_context = let_mock()

    @set_up
    def set_up(self):
        self._create_job_workspace_called = False
        self._chdir_called = False

        self.mock_predictor_class = self.patch('foundations_production.serving.inference.predictor.Predictor')
        self.mock_predictor_class.predictor_for = ConditionalReturn()
        self.mock_predictor_class.predictor_for.return_when(self.mock_predictor, self.model_package_id)
        self.mock_predictor.json_predictions_for = ConditionalReturn()
        self.mock_predictor.json_predictions_for.return_when(self.prediction, self.fake_data)

        self.mock_create_job_workspace.side_effect = self._set_create_job_workspace_called
        self.mock_chdir.side_effect = self._check_create_job_workspace_called_and_set_chdir_called

        self.mock_foundations_context.pipeline_context.return_value = self.mock_pipeline_context

    def test_run_model_package_loads_model_package(self):
        self.communicator.set_action_request(self.fake_data)
        self.communicator.set_action_request('STOP')

        run_model_package(self.model_package_id, self.communicator)
        self.mock_predictor_class.predictor_for.assert_called_with(self.model_package_id)
    
    def test_run_model_package_puts_predictions_into_pipe(self):
        self.communicator.set_action_request(self.fake_data)
        self.communicator.set_action_request('STOP')

        run_model_package(self.model_package_id, self.communicator)
        self._remove_success_token_from_pipe()

        self.assertEqual(self.prediction, self.communicator.get_response())
    
    def test_run_model_package_runs_until_stop_received(self):
        for _ in range(self.number_of_calls):
            self.communicator.set_action_request(self.fake_data)
        self.communicator.set_action_request('STOP')

        run_model_package(self.model_package_id, self.communicator)

        self._remove_success_token_from_pipe()

        responses = [self.communicator.get_response() for _ in range(self.number_of_calls)]
        expected_responses = [self.prediction] * self.number_of_calls
        self.assertEqual(expected_responses, responses)
    
    def test_run_model_package_returns_error_in_json_when_prediction_for_throws_exception(self):
        def raise_exception(data):
            raise Exception('Test exception')

        self.mock_predictor.json_predictions_for = raise_exception
        self.communicator.set_action_request(self.fake_data_that_errors)

        run_model_package(self.model_package_id, self.communicator)

        self._remove_success_token_from_pipe()

        expected_return = {
            'name': 'Exception',
            'value': 'Test exception'
        }
        self.assertEqual(expected_return, self.communicator.get_response())
    
    def test_run_model_package_returns_error_in_json_when_prediction_for_throws_type_error(self):
        def raise_exception(data):
            raise TypeError('Wrong type')

        self.mock_predictor.json_predictions_for = raise_exception
        self.communicator.set_action_request(self.fake_data_that_errors)

        run_model_package(self.model_package_id, self.communicator)

        self._remove_success_token_from_pipe()

        expected_return = {
            'name': 'TypeError',
            'value': 'Wrong type'
        }
        self.assertEqual(expected_return, self.communicator.get_response())
    
    def test_run_model_package_returns_error_when_predictor_for_throws_exception(self):
        def raise_exception(data):
            raise Exception('Test exception')

        self.mock_predictor_class.predictor_for = raise_exception

        run_model_package(self.model_package_id, self.communicator)

        expected_return = {
            'name': 'Exception',
            'value': 'Test exception'
        }
        self.assertEqual(expected_return, self.communicator.get_response())
    
    def test_run_model_package_returns_error_when_predictor_for_throws_value_error(self):
        def raise_exception(data):
            raise ValueError('Different message')

        self.mock_predictor_class.predictor_for = raise_exception

        run_model_package(self.model_package_id, self.communicator)

        expected_return = {
            'name': 'ValueError',
            'value': 'Different message'
        }
        self.assertEqual(expected_return, self.communicator.get_response())
    
    def test_run_model_package_returns_error_when_create_job_workspace_for_throws_value_error(self):
        self.mock_create_job_workspace.side_effect = ValueError('Different message')

        run_model_package(self.model_package_id, self.communicator)

        expected_return = {
            'name': 'ValueError',
            'value': 'Different message'
        }
        self.assertEqual(expected_return, self.communicator.get_response())

    def test_run_model_package_returns_key_error_when_create_job_workspace_for_throws_file_not_found_error(self):
        self.mock_create_job_workspace.side_effect = FileNotFoundError('Different message')

        run_model_package(self.model_package_id, self.communicator)

        expected_return = {
            'name': 'KeyError',
            'value': "'Model Package ID {} does not exist'".format(self.model_package_id)
        }
        self.assertEqual(expected_return, self.communicator.get_response())

    def test_run_model_package_returns_error_when_predictor_for_throws_value_error(self):
        self.communicator.set_action_request('STOP')
        run_model_package(self.model_package_id, self.communicator)

        expected_return = 'SUCCESS: predictor created'
        self.assertEqual(expected_return, self.communicator.get_response())
    
    def test_run_model_package_creates_job_workspace(self):
        self.communicator.set_action_request('STOP')
        run_model_package(self.model_package_id, self.communicator)

        self.mock_create_job_workspace.assert_called_with(self.model_package_id)
    
    def test_run_model_package_changes_directory_to_workspace_directory(self):
        self.communicator.set_action_request('STOP')
        run_model_package(self.model_package_id, self.communicator)

        self.mock_chdir.assert_called_with(self.workspace_directory)

    def test_run_model_package_adds_workspace_directory_to_python_path(self):
        mock_sys_path = self.patch('sys.path')

        self.communicator.set_action_request('STOP')
        run_model_package(self.model_package_id, self.communicator)

        mock_sys_path.append.assert_called_with(self.workspace_directory)
    
    def test_run_model_package_sets_job_id_to_dummy_value(self):
        self.communicator.set_action_request('STOP')
        run_model_package(self.model_package_id, self.communicator)

        self.assertEqual('package_running', self.mock_pipeline_context.file_name)

    def _set_create_job_workspace_called(self, *args):
        self._create_job_workspace_called = True
    
    def _check_create_job_workspace_called_and_set_chdir_called(self, *args):
        if not self._create_job_workspace_called:
            raise AssertionError('Job workspace needs to be created before directory changed')
        self._chdir_called = True
    
    def _check_chdir_called(self, *args):
        if not self._chdir_called:
            raise AssertionError('Directory needs to be changed before predictor created')

    def _remove_success_token_from_pipe(self):
        self.communicator.get_response()