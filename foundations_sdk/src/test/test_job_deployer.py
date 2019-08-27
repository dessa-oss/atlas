"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations.job_deployer import deploy_job

class TestJobDeployer(Spec):

    mock_log_manager = let_patch_mock('foundations.log_manager')
    mock_deployment_manager = let_patch_mock('foundations.global_state.deployment_manager')

    mock_logger = Mock()
    mock_deployment = Mock()

    @set_up
    def set_up(self):
        mock_get_logger = ConditionalReturn()
        mock_get_logger.return_when(self.mock_logger, 'foundations.job_deployer')
        self.mock_log_manager.get_logger = mock_get_logger

        mock_simple_deploy = ConditionalReturn()
        mock_simple_deploy.return_when(self.mock_deployment, self.fake_pipeline_context_wrapper, self.fake_job_name, self.fake_job_params)
        self.mock_deployment_manager.simple_deploy = mock_simple_deploy

        self.mock_deployment.job_name.return_value = self.fake_job_name

    @let
    def fake_job_name(self):
        return self.faker.uuid4()

    @let
    def fake_pipeline_context_wrapper(self):
        return Mock()

    @let
    def fake_job_params(self):
        return Mock()

    def test_job_deployer_logs_job_deploying_message(self):
        deploy_job(self.fake_pipeline_context_wrapper, self.fake_job_name, self.fake_job_params)
        self.mock_logger.info.assert_called_with('Deploying job...')
    
    def test_job_deployer_returns_job_deployment_with_same_job_name_as_was_passed_in(self):
        job_deployment = deploy_job(self.fake_pipeline_context_wrapper, self.fake_job_name, self.fake_job_params)
        self.assertEqual(self.fake_job_name, job_deployment.job_name())

    def test_job_deployer_returns_deployment_wrapper(self):
        from foundations_contrib.deployment_wrapper import DeploymentWrapper

        job_deployment = deploy_job(self.fake_pipeline_context_wrapper, self.fake_job_name, self.fake_job_params)
        self.assertIsInstance(job_deployment, DeploymentWrapper)