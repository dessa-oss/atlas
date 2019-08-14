"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_model_package.flask_app import flask_app

class TestFlaskApp(Spec):

    mock_flask_class = let_patch_mock_with_conditional_return('flask.Flask')
    mock_flask_instance = let_mock()
    mock_flask_cors = let_patch_mock('flask_cors.CORS')
    mock_flask_api = let_patch_mock_with_conditional_return('flask_restful.Api')
    mock_flask_api_instance = let_mock()

    mock_root_resource = let_mock()
    mock_predict_resource = let_mock()
    mock_evaluate_resource = let_mock()

    @set_up
    def set_up(self):
        self.mock_flask_class.return_when(self.mock_flask_instance, 'foundations_model_package.flask_app')
        self.mock_flask_api.return_when(self.mock_flask_api_instance, self.mock_flask_instance)

        self._flask_app = flask_app(self.mock_root_resource, self.mock_predict_resource, self.mock_evaluate_resource)

    def test_flask_app_sets_up_cors(self):
        self.mock_flask_cors.assert_called_once_with(self.mock_flask_instance, supports_credentials=True)

    def test_flask_app_returns_flask_application_instance(self):
        app = self._flask_app
        self.assertEqual(self.mock_flask_instance, app)

    def test_flask_app_disables_app_logger(self):
        app = self._flask_app
        self.assertEqual(True, app.logger.disabled)

    def test_flask_app_adds_root_resource_to_api(self):
        self.mock_flask_api_instance.add_resource.assert_any_call(self.mock_root_resource, '/')

    def test_flask_app_adds_predict_resource_to_api(self):
        self.mock_flask_api_instance.add_resource.assert_any_call(self.mock_predict_resource, '/predict')

    def test_flask_app_adds_evaluate_resource_to_api(self):
        self.mock_flask_api_instance.add_resource.assert_any_call(self.mock_evaluate_resource, '/evaluate')