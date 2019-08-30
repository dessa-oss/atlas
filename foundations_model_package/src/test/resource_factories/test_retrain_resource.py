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

    mock_get_cwd = let_patch_mock('os.getcwd')


    @let
    def project_name(self):
        return self.faker.word()

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def retrain_driver_path(self):
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
        self.mock_retrain_driver.__enter__ = lambda *args: self.retrain_driver_path
        self.mock_retrain_driver.__exit__ = lambda *args: None

        self.mock_job_deployment.job_name.return_value = self.job_id
        self.mock_submit.return_value = self.mock_job_deployment

        self.mock_environ = self.patch('os.environ', {})
        self.mock_environ['PROJECT_NAME'] = self.project_name
        self.mock_environ['MODEL_NAME'] = self.model_name

        self.mock_get_cwd.return_value = self.cwd

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
        self._perform_retrain(self.mock_retrain_driver)
        self.mock_submit.assert_called_with(project_name=self.project_name, entrypoint=self.retrain_driver_path, params=self.params)

    def test_retrain_resource_serves_new_model(self):
        payload, code = self._perform_retrain(self.mock_retrain_driver)
        
    def test_retrain_resource_returns_job_id(self):
        payload, _ = self._perform_retrain(self.mock_retrain_driver)
        self.assertEqual(self.job_id, payload['job_id'])

    def test_retrain_resource_returns_status_code_202(self):
        _, code = self._perform_retrain(self.mock_retrain_driver)
        self.assertEqual(202, code)

    def test_retrain_resource_returns_404_if_driver_is_none(self):
        _, code = self._perform_retrain(None)
        self.assertEqual(404, code)

    def test_retrain_resource_returns_error_message_if_callback_is_none(self):
        error_message, _ = self._perform_retrain(None)
        self.assertEqual({'error': 'retrain not set in manifest'}, error_message)

    def test_retrain_resource_adds_listener_for_completed_job(self):
        mock_add_listener = self.patch('foundations.global_state.message_router.add_listener')
        mock_retrain_deployer_class = self.patch('foundations_model_package.retrain_deployer.RetrainDeployer', ConditionalReturn())
        mock_retrain_deployer = Mock()
        mock_retrain_deployer_class.return_when(mock_retrain_deployer, self.job_id, self.project_name, self.model_name, self.cwd)

        self._perform_retrain(self.mock_retrain_driver)
        mock_add_listener.assert_called_once_with(mock_retrain_deployer, 'complete_job')

    def test_deployer_is_called_when_job_complete_event_is_triggered(self):
        from foundations.global_state import message_router

        mock_time = self.patch('time.time')
        mock_time.return_value = self.time

        mock_retrain_deployer_class = self.patch('foundations_model_package.retrain_deployer.RetrainDeployer', ConditionalReturn())
        mock_retrain_deployer = Mock()
        mock_retrain_deployer_class.return_when(mock_retrain_deployer, self.job_id, self.project_name, self.model_name, self.cwd)
        self._perform_retrain(self.mock_retrain_driver)

        message = {
            'job_id': self.job_id,
            'project_name': self.project_name
        }

        message_router.push_message('complete_job', message)

        mock_retrain_deployer.call.assert_called_once_with(message, self.time, None)
        
    def _perform_retrain(self, retrain_driver):
        self.mock_flask_request.json = self.params

        resource_class = retrain_resource(retrain_driver)
        resource = resource_class()
        return resource.post()