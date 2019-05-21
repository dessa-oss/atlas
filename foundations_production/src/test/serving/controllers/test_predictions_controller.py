"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from mock import patch

from foundations_spec import *
from foundations_production.serving.rest_api_server import RestAPIServer

class TestPredictionsController(Spec):

    package_pool_mock = let_mock()
    communicator_mock = let_mock()

    @let
    def model_package_id(self):
        return self.faker.uuid4()

    @let
    def user_defined_model_name(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        from foundations_production.serving.controllers.predictions_controller import PredictionsController

        self.predictions_controller = PredictionsController()
        self.package_pool_mock.get_communicator.return_value = self.communicator_mock

        RestAPIServer()

    def test_predictions_controller_returns_404_when_model_package_not_deployed(self):
        from werkzeug.exceptions import NotFound
        self.predictions_controller.params = {
            'user_defined_model_name': self.user_defined_model_name,
            'rows': 'irrelevant',
            'schema': 'also irrelevant'
        }
        with self.assertRaises(NotFound):
            response = self.predictions_controller.post()
            self.assertEqual(404, response.status())

    def test_predictions_controller_returns_status_code_200_if_model_package_is_deployed(self):
        status, _ = self._run_prediction({}, {})
        self.assertEqual(200, status)

    def test_predictions_from_model_package_sets_action_request_for_prediction(self):
        input_data = {
            'rows': [['value', 43234], ['spider', 323]],
            'schema': [{'name': '1st column', 'type': 'string'}, {'name': '2nd column', 'type': 'int'}]
        }
        self._run_prediction(input_data, {})
        self.communicator_mock.set_action_request.assert_called_with(input_data)

    def test_predictions_controller_returns_predictions_if_model_package_is_deployed(self):
        input_data = {
            'rows': [['value', 43234], ['spider', 323]],
            'schema': [{'name': '1st column', 'type': 'string'}, {'name': '2nd column', 'type': 'int'}]
        }
        expected_prediction_json = {
            'rows': [['value transformed predicted', 43667], ['spider transformed predicted', 756]],
            'schema': [{'name': '1st column', 'type': 'object'}, {'name': '2nd column', 'type': 'int64'}]
        }
        _, output = self._run_prediction(input_data, expected_prediction_json)
        self.assertEqual(expected_prediction_json, output)

    def _run_prediction(self, input_data, expected_output):
        with patch.object(RestAPIServer, 'get_package_pool') as get_package_pool_mock:
            with patch.object(RestAPIServer, 'get_model_package_mapping') as get_model_package_mapping_mock:
                get_model_package_mapping_mock.return_value = {self.user_defined_model_name: self.model_package_id}
                get_package_pool_mock.return_value = self.package_pool_mock
                self.predictions_controller.params = {
                    'user_defined_model_name': self.user_defined_model_name,
                }
                self.predictions_controller.params.update(input_data)
                self.communicator_mock.get_response.return_value = expected_output
                response = self.predictions_controller.post()
                response.evaluate()
        return response.status(), response.as_json()
