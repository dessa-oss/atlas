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
    mock_logger = Mock()

    @set_up
    def set_up(self):
        mock_get_logger = ConditionalReturn()
        mock_get_logger.return_when(self.mock_logger, 'foundations.job_deployer')
        self.mock_log_manager.get_logger = mock_get_logger

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