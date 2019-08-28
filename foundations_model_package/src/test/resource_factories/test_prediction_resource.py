"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_model_package.resource_factories import prediction_resource

class TestPredictionResource(Spec):

    mock_flask_request = let_patch_mock('flask.request')

    @let
    def fake_return_result(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        self._prediction_callback_kwargs = None

    def test_prediction_resource_has_get_method_which_returns_still_alive_message(self):
        resource_class = prediction_resource(None)
        resource = resource_class()
        self.assertEqual({'message': 'still alive'}, resource.get())

    def test_prediction_resource_is_instance_of_flask_restful_resource(self):
        from flask_restful import Resource

        resource_class = prediction_resource(None)
        resource = resource_class()
        self.assertIsInstance(resource, Resource)

    def test_prediction_resource_has_post_method_which_splats_request_json_into_prediction_callback(self):
        self.mock_flask_request.json = {'arg_0': 0, 'arg_1': 1}

        resource_class = prediction_resource(self._prediction_callback)
        resource = resource_class()
        resource.post()

        self.assertEqual({'arg_0': 0, 'arg_1': 1}, self._prediction_callback_kwargs)

    def test_prediction_resource_has_post_method_which_splats_request_json_into_prediction_callback_different_payload(self):
        self.mock_flask_request.json = {'arg_3': [100, 200]}

        resource_class = prediction_resource(self._prediction_callback)
        resource = resource_class()
        resource.post()

        self.assertEqual({'arg_3': [100, 200]}, self._prediction_callback_kwargs)

    def test_prediction_resource_post_method_returns_result_from_callback(self):
        self.mock_flask_request.json = {'arg_3': [100, 200]}

        resource_class = prediction_resource(self._returning_callback)
        resource = resource_class()
        self.assertEqual(self.fake_return_result, resource.post())

    def test_prediction_resource_has_different_name_each_time_when_constructed(self):
        resource_class_0 = prediction_resource(self._returning_callback)
        resource_class_1 = prediction_resource(self._returning_callback)

        self.assertNotEqual(resource_class_0.__name__, resource_class_1.__name__)

    def _prediction_callback(self, **kwargs):
        self._prediction_callback_kwargs = kwargs

    def _returning_callback(self, **kwargs):
        return self.fake_return_result