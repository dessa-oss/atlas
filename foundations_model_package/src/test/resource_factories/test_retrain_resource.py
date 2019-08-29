"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_model_package.resource_factories import retrain_resource

class TestRetrainResource(Spec):
    
    mock_submit = let_patch_mock('foundations.submit')
    mock_job_deployment = let_mock()
    mock_flask_request = let_patch_mock('flask.request')
    mock_retrain_driver = let_mock()

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def retrain_driver_path(self):
        return self.faker.file_path()

    @set_up
    def set_up(self):
        self.mock_retrain_driver.__enter__ = lambda *args: self.retrain_driver_path
        self.mock_retrain_driver.__exit__ = lambda *args: None

        self.mock_job_deployment.job_name.return_value = self.job_id
        self.mock_submit.return_value = self.mock_job_deployment

        self.mock_environ = self.patch('os.environ', {})
        self.mock_environ['PROJECT_NAME'] = self.project_name

    def test_retrain_resource_is_instance_of_flask_restful_resource(self):
        from flask_restful import Resource

        resource_class = retrain_resource(self.mock_retrain_driver)
        resource = resource_class()
        self.assertIsInstance(resource, Resource)

    def test_retrain_resource_has_different_name_each_time_when_constructed(self):
        resource_class_0 = retrain_resource(self.mock_retrain_driver)
        resource_class_1 = retrain_resource(self.mock_retrain_driver)

        self.assertNotEqual(resource_class_0.__name__, resource_class_1.__name__)

    def test_retrain_resource_calls_foundations_submit_with_entrypoint_equal_to_retrain_driver_path(self):
        self.mock_flask_request.json = {'arg_0': 0, 'arg_1': 1}

        resource_class = retrain_resource(self.mock_retrain_driver)
        resource = resource_class()
        resource.post()

        self.mock_submit.assert_called_with(project_name=self.project_name, entrypoint=self.retrain_driver_path, params={'arg_0': 0, 'arg_1': 1})

    def test_retrain_resource_returns_job_id(self):
        self.mock_flask_request.json = {'arg_0': 0, 'arg_1': 1}

        resource_class = retrain_resource(self.mock_retrain_driver)
        resource = resource_class()
        payload, _ = resource.post()

        self.assertEqual(self.job_id, payload['job_id'])

    def test_retrain_resource_returns_status_code_202(self):
        self.mock_flask_request.json = {'arg_0': 0, 'arg_1': 1}

        resource_class = retrain_resource(self.mock_retrain_driver)
        resource = resource_class()
        _, code = resource.post()

        self.assertEqual(202, code)

