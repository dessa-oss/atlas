"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_production.serving.package_runner import run_model_package, run_prediction

class TestPackageRunner(Spec):

    @let
    def fake_data(self):
        return self.faker.word()
    
    @let
    def prediction(self):
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
    
    mock_model_package = let_mock()
    
    mock_load_model_package = let_patch_mock('foundations_production.load_model_package')

    @set_up
    def set_up(self):
        self.mock_load_model_package.return_value = self.mock_model_package

        self.mock_model_package.model.predict = ConditionalReturn()
        self.mock_model_package.model.predict.return_when(self.prediction, self.fake_data)

    def test_run_prediction_runs_prediction_on_model_with_correct_data(self):
        actual_prediction = run_prediction(self.mock_model_package, self.fake_data)
        self.assertEqual(self.prediction, actual_prediction)
    
    def test_run_model_package_loads_model_package(self):
        self.communicator.set_action_request(self.fake_data)
        self.communicator.set_action_request('STOP')

        run_model_package(self.model_package_id, self.communicator)
        self.mock_load_model_package.assert_called_with(self.model_package_id)
    
    def test_run_model_package_puts_predictions_into_pipe(self):
        self.communicator.set_action_request(self.fake_data)
        self.communicator.set_action_request('STOP')

        run_model_package(self.model_package_id, self.communicator)

        self.assertEqual(self.prediction, self.communicator.get_response())
    
    def test_run_model_package_runs_until_stop_received(self):
        for _ in range(self.number_of_calls):
            self.communicator.set_action_request(self.fake_data)
        self.communicator.set_action_request('STOP')

        run_model_package(self.model_package_id, self.communicator)

        responses = [self.communicator.get_response() for _ in range(self.number_of_calls)]
        expected_responses = [self.prediction] * self.number_of_calls
        self.assertEqual(expected_responses, responses)