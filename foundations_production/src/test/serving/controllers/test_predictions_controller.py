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
        RestAPIServer()

    def test_predictions_controller_returns_404_when_model_package_not_deployed(self):
        from werkzeug.exceptions import NotFound
        self.predictions_controller.params = {
            'model_id': self.model_package_id,
            'user_defined_model_name': self.user_defined_model_name,
            'rows': [['value', 43234], ['spider', 323]],
            'schema': [{'name': '1st column', 'type': 'string'}, {'name': '2nd column', 'type': 'int'}]
        }
        with self.assertRaises(NotFound):
            response = self.predictions_controller.put()
            self.assertEqual(404, response.status())

    @patch.object(RestAPIServer, 'get_model_package_mapping')
    def test_predictions_controller_returns_predictions_if_model_package_is_deployed(self, get_model_package_mapping_mock):
        get_model_package_mapping_mock.return_value = {self.user_defined_model_name: self.model_package_id}
        self.predictions_controller.params = {
            'model_id': self.model_package_id,
            'user_defined_model_name': self.user_defined_model_name,
            'rows': [['value', 43234], ['spider', 323]],
            'schema': [{'name': '1st column', 'type': 'string'}, {'name': '2nd column', 'type': 'int'}]
        }
        expected_prediction_json = {
            'rows': [['value transformed predicted', 43667], ['spider transformed predicted', 756]],
            'schema': [{'name': '1st column', 'type': 'object'}, {'name': '2nd column', 'type': 'int64'}]
        }
        response = self.predictions_controller.put()
        self.assertEqual(202, response.status())
        self.assertEqual({'created_job_uuid': self.retraining_job_id}, response.as_json())
