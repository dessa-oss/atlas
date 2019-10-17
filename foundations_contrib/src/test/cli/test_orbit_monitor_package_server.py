"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from foundations_spec import *

class TestOrbitMonitorPackageServer(Spec):

    @set_up
    def set_up(self):
        mock_config_manager = self.patch('foundations_contrib.foundations_contrib.global_state.config_manager')
        mock_config_manager.config.return_value = {'scheduler_url': 'https://localhost:5000'}

    @let
    def monitor_name(self):
        return self.faker.word()

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def env(self):
        return self.faker.word()

    @let
    def monitor_package_id(self):
        return f'{self.project_name}-{self.monitor_name}'

    @let_now
    def cron_job_scheduler(self):
        mock_cron_job_scheduler = Mock()
        mock_cron_job_scheduler_class = self.patch('foundations_local_docker_scheduler_plugin.cron_job_scheduler.CronJobScheduler')
        mock_cron_job_scheduler_class.return_value = mock_cron_job_scheduler
        return mock_cron_job_scheduler
    
    @let_now
    def load(self):
        return self.patch('foundations_contrib.cli.job_submission.config.load')

    def test_pause_called_cron_job_scheduler_pause_job(self):
        from foundations_contrib.cli.orbit_monitor_package_server import pause
        pause(self.project_name, self.monitor_name, self.env)
        self.cron_job_scheduler.pause_job.assert_called_once_with(self.monitor_package_id)

    def test_pause_called_cron_job_scheduler_resume_job(self):
        from foundations_contrib.cli.orbit_monitor_package_server import resume
        resume(self.project_name, self.monitor_name, self.env)
        self.cron_job_scheduler.resume_job.assert_called_once_with(self.monitor_package_id)

    def test_pause_uses_update_config_with_values_from_env(self):
        from foundations_contrib.cli.orbit_monitor_package_server import pause
        pause(self.project_name, self.monitor_name, self.env)
        self.load.assert_called_once_with(self.env)
    
    def test_resume_uses_update_config_with_values_from_env(self):
        from foundations_contrib.cli.orbit_monitor_package_server import resume
        resume(self.project_name, self.monitor_name, self.env)
        self.load.assert_called_once_with(self.env)

    def test_delete_called_cron_job_scheduler_pause_job(self):
        from foundations_contrib.cli.orbit_monitor_package_server import delete
        delete(self.project_name, self.monitor_name, self.env)
        self.cron_job_scheduler.delete_job.assert_called_once_with(self.monitor_package_id)

    def test_delete_uses_update_config_with_values_from_env(self):
        from foundations_contrib.cli.orbit_monitor_package_server import delete
        delete(self.project_name, self.monitor_name, self.env)
        self.load.assert_called_once_with(self.env)