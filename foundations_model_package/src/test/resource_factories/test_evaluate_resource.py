"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_model_package.resource_factories import evaluate_resource

class TestEvaluateResource(Spec):

    mock_flask_request = let_patch_mock('flask.request')
    mock_process_class = let_patch_mock_with_conditional_return('multiprocessing.Process')
    mock_process_object = let_mock()
    mock_evaluate_callback = let_mock()

    @let
    def fake_return_result(self):
        return self.faker.word()

    def test_evaluate_resource_is_instance_of_flask_restful_resource(self):
        from flask_restful import Resource

        resource_class = evaluate_resource(None)
        resource = resource_class()
        self.assertIsInstance(resource, Resource)

    def test_evaluate_resource_has_post_method_which_calls_evaluate_callback_async(self):
        self.mock_flask_request.json = {'arg_0': 0, 'arg_1': 1}
        self.mock_process_class.return_when(self.mock_process_object, target=self.mock_evaluate_callback, kwargs={'arg_0': 0, 'arg_1': 1})

        resource_class = evaluate_resource(self.mock_evaluate_callback)
        resource = resource_class()
        resource.post()

        self.mock_process_object.start.assert_called_once()

    def test_evaluate_resource_has_post_method_which_returns_202_when_callback_exists(self):
        self.mock_flask_request.json = {'arg_0': 0, 'arg_1': 1}
        self.mock_process_class.return_when(self.mock_process_object, target=self.mock_evaluate_callback, kwargs={'arg_0': 0, 'arg_1': 1})

        resource_class = evaluate_resource(self.mock_evaluate_callback)
        resource = resource_class()
        _, code = resource.post()

        self.assertEqual(202, code)

    def test_evaluate_resource_has_post_method_which_returns_empty_payload_when_callback_exists(self):
        self.mock_flask_request.json = {'arg_0': 0, 'arg_1': 1}
        self.mock_process_class.return_when(self.mock_process_object, target=self.mock_evaluate_callback, kwargs={'arg_0': 0, 'arg_1': 1})

        resource_class = evaluate_resource(self.mock_evaluate_callback)
        resource = resource_class()
        payload, _ = resource.post()

        self.assertEqual({}, payload)

    def test_evaluate_resource_has_post_method_which_splats_request_json_into_evaluate_callback_different_payload(self):
        self.mock_flask_request.json = {'arg_3': [100, 200]}
        self.mock_process_class.return_when(self.mock_process_object, target=self.mock_evaluate_callback, kwargs={'arg_3': [100, 200]})

        resource_class = evaluate_resource(self.mock_evaluate_callback)
        resource = resource_class()
        resource.post()

        self.mock_process_object.start.assert_called_once()

    def test_evaluate_resource_has_different_name_each_time_when_constructed(self):
        resource_class_0 = evaluate_resource(self.mock_evaluate_callback)
        resource_class_1 = evaluate_resource(self.mock_evaluate_callback)

        self.assertNotEqual(resource_class_0.__name__, resource_class_1.__name__)

    def test_evaluate_resource_returns_404_if_callback_is_none(self):
        resource_class = evaluate_resource(None)
        resource = resource_class()
        _, code = resource.post()
        self.assertEqual(404, code)

    def test_evaluate_resource_returns_error_message_if_callback_is_none(self):
        resource_class = evaluate_resource(None)
        resource = resource_class()
        error_message, _ = resource.post()
        self.assertEqual({'error': 'evaluate not set in manifest'}, error_message)