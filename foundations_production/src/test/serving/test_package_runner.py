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
    
    mock_predictor = let_mock()
    
    @set_up
    def set_up(self):
        self.mock_predictor_class = self.patch('foundations_production.serving.inference.predictor.Predictor')
        self.mock_predictor_class.predictor_for = ConditionalReturn()
        self.mock_predictor_class.predictor_for.return_when(self.mock_predictor, self.model_package_id)
        self.mock_predictor.json_predictions_for = ConditionalReturn()
        self.mock_predictor.json_predictions_for.return_when(self.prediction, self.fake_data)

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

    def test_run_model_package_returns_error_when_predictor_for_throws_value_error(self):
        self.communicator.set_action_request('STOP')
        run_model_package(self.model_package_id, self.communicator)

        expected_return = 'SUCCESS: predictor created'
        self.assertEqual(expected_return, self.communicator.get_response())
    
    def _remove_success_token_from_pipe(self):
        self.communicator.get_response()