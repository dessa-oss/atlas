"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_contrib.jobs.logs import job_logs

class TestLogs(Spec):

    job_deployment = let_mock()

    @let
    def mock_deployment_klass(self):
        return ConditionalReturn()
    
    @let_now
    def config_manager(self):
        from foundations_contrib.config_manager import ConfigManager

        config_manager = ConfigManager()
        config_manager['deployment_implementation'] = { 'deployment_type': self.mock_deployment_klass }
        return self.patch('foundations_contrib.global_state.config_manager', config_manager)

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def job_logs(self):
        return self.faker.sentence()

    @set_up 
    def set_up(self):
        self.mock_deployment_klass.return_when(self.job_deployment, self.job_id, None, None)
        self.job_deployment.get_job_logs.return_value = self.job_logs

    def test_returns_none_when_job_has_no_status(self):
        self.job_deployment.get_job_status.return_value = None
        self.assertIsNone(job_logs(self.job_id))
    
    def test_returns_none_when_job_is_queued(self):
        self.job_deployment.get_job_status.return_value = 'queued'
        self.assertIsNone(job_logs(self.job_id))

    def test_returns_jobs_logs_when_job_is_running(self):
        self.job_deployment.get_job_status.return_value = 'running'
        self.assertEqual(self.job_logs, job_logs(self.job_id))
        