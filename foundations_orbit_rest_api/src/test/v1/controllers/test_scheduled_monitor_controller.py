"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 10 2019
"""

from foundations_spec import *


class TestScheduledMonitorController(Spec):

    @set_up
    def set_up(self):
        self.cron_job_scheduler_class = self.patch('foundations_local_docker_scheduler_plugin.cron_job_scheduler.CronJobScheduler')
        self.cron_job_scheduler = Mock()
        self.cron_job_scheduler_class.return_when = self.cron_job_scheduler

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def monitor_name(self):
        return self.faker.word()

    @let
    def monitor_id(self):
        return f'{self.project_name}-{self.monitor_name}'

    @let
    def monitor_controller(self):
        from foundations_orbit_rest_api.v1.controllers.scheduled_monitor_controller import ScheduledMonitorController
        return ScheduledMonitorController()

    def _set_params_and_put(self, content=None):
        self.monitor_controller.params = {'project_name': self.project_name, 'monitor_name': self.monitor_name}
        if content:
            self.monitor_controller.params.update(content)
        return self.monitor_controller.put()

    def test_put_request_for_resume_returns_status_code_204_if_successful(self):
        self.patch('foundations_core_cli.orbit_monitor_package_server.resume')
        response = self._set_params_and_put({'status': 'resume'})
        self.assertEqual(204, response.status())

    def test_put_request_with_resume_triggers_put_operation_with_resume_in_scheduled_monitor(self):
        mock_scheduled_monitor = self.patch('foundations_orbit_rest_api.v1.models.scheduled_monitor.ScheduledMonitor')
        self._set_params_and_put({'status': 'resume'}).evaluate()
        mock_scheduled_monitor.put.assert_called_once_with(project_name=self.project_name, name=self.monitor_name, status='resume')

    def test_put_request_with_status_as_active_triggers_put_operation_with_active_in_scheduled_monitor(self):
        mock_scheduled_monitor = self.patch('foundations_orbit_rest_api.v1.models.scheduled_monitor.ScheduledMonitor')
        self._set_params_and_put({'status': 'active'}).evaluate()
        mock_scheduled_monitor.put.assert_called_once_with(project_name=self.project_name, name=self.monitor_name, status='active')

    def test_put_request_for_pause_returns_status_code_204_if_successful(self):
        self.patch('foundations_core_cli.orbit_monitor_package_server.pause')
        response = self._set_params_and_put({'status': 'pause'})
        self.assertEqual(204, response.status())

    def test_put_request_with_appropriate_body_content_triggers_put_operation_in_scheduled_monitor(self):
        mock_scheduled_monitor = self.patch('foundations_orbit_rest_api.v1.models.scheduled_monitor.ScheduledMonitor')
        self._set_params_and_put({'status': 'pause'}).evaluate()
        mock_scheduled_monitor.put.assert_called_once_with(project_name=self.project_name, name=self.monitor_name, status='pause')

    def test_put_request_throws_key_error_if_no_status_passed(self):
        with self.assertRaises(KeyError) as ex:
            response = self._set_params_and_put()
        self.assertEqual('\'status\'', str(ex.exception))