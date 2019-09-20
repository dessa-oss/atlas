"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_model_package.resource_factories import recalibrate_resource

class TestRecalibrateResource(Spec):
    
    mock_submit = let_patch_mock('foundations.submit')
    mock_job_deployment = let_mock()
    mock_flask_request = let_patch_mock('flask.request')
    mock_recalibrate_driver = let_mock()

    mock_get_cwd = let_patch_mock('os.getcwd')
    mock_wait = let_patch_mock('foundations_model_package.recalibrate_deployer._wait_for_job_to_complete')

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def recalibrate_driver_path(self):
        return self.faker.file_path()

    @let
    def model_name(self):
        return self.faker.word()

    @let
    def cwd(self):
        return self.faker.file_path

    @let
    def time(self):
        return self.faker.random.random()

    @let
    def params(self):
        return {
            'model-name': self.model_name, 
            'arg_0': 0, 
            'arg_1': 1
            }

    @set_up
    def set_up(self):
        self.mock_recalibrate_driver.__enter__ = lambda *args: self.recalibrate_driver_path
        self.mock_recalibrate_driver.__exit__ = lambda *args: None

        self.mock_job_deployment.job_name.return_value = self.job_id
        self.mock_submit.return_value = self.mock_job_deployment

        self.mock_environ = self.patch('os.environ', {})
        self.mock_environ['PROJECT_NAME'] = self.project_name
        self.mock_environ['MODEL_NAME'] = self.model_name

        self.mock_get_cwd.return_value = self.cwd

        mock_load_incluster_config = self.patch('kubernetes.config.load_incluster_config')
        mock_placeholder = Mock()
        mock_load_incluster_config.return_value = mock_placeholder

    def test_recalibrate_resource_is_instance_of_flask_restful_resource(self):
        from flask_restful import Resource

        resource_class = recalibrate_resource(self.mock_recalibrate_driver)
        resource = resource_class()
        self.assertIsInstance(resource, Resource)

    def test_recalibrate_resource_has_different_name_each_time_when_constructed(self):
        resource_class_0 = recalibrate_resource(self.mock_recalibrate_driver)
        resource_class_1 = recalibrate_resource(self.mock_recalibrate_driver)

        self.assertNotEqual(resource_class_0.__name__, resource_class_1.__name__)

    def test_recalibrate_resource_calls_foundations_submit_with_entrypoint_equal_to_recalibrate_driver_path(self):
        self._perform_recalibrate(self.mock_recalibrate_driver)
        self.params.pop('model-name')
        self.mock_submit.assert_called_with(project_name=self.project_name, entrypoint=self.recalibrate_driver_path, params=self.params)

    def test_recalibrate_resource_serves_new_model(self):
        payload, code = self._perform_recalibrate(self.mock_recalibrate_driver)
        
    def test_recalibrate_resource_returns_job_id(self):
        payload, _ = self._perform_recalibrate(self.mock_recalibrate_driver)
        self.assertEqual(self.job_id, payload['job_id'])

    def test_recalibrate_resource_returns_status_code_202(self):
        _, code = self._perform_recalibrate(self.mock_recalibrate_driver)
        self.assertEqual(202, code)

    def test_recalibrate_resource_returns_404_if_driver_is_none(self):
        _, code = self._perform_recalibrate(None)
        self.assertEqual(404, code)

    def test_recalibrate_resource_returns_error_message_if_callback_is_none(self):
        error_message, _ = self._perform_recalibrate(None)
        self.assertEqual({'error': 'recalibrate not set in manifest'}, error_message)

    def _perform_recalibrate(self, recalibrate_driver):
        self.mock_flask_request.json = self.params

        resource_class = recalibrate_resource(recalibrate_driver)
        resource = resource_class()
        return resource.post()