"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 10 2019
"""

from foundations_spec import *
from foundations_monitor_rest_api.v1.controllers.monitors_controller import MonitorsController


class TestMonitorsController(Spec):

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def monitor_name(self):
        return self.faker.word()

    @let
    def monitor_id(self):
        return f'{self.project_name}-{self.monitor_name}'

    @set_up
    def set_up(self):
        self.cron_job_scheduler_class = self.patch('foundations_local_docker_scheduler_plugin.cron_job_scheduler.CronJobScheduler')
        self.cron_job_scheduler = Mock()
        self.cron_job_scheduler_class.return_when = self.cron_job_scheduler

    # request for monitors should return empty list for project that has no monitors
    # request for monitors for a project that doesn't exist then produces 404
    # request for monitors should return list with expected projects based on configured monitors for a project
    
    def test_request_for_monitors_by_project_returns_monitors_by_calling_function_of_the_monitor_package_server(self):
        expected_results = {
            self.monitor_id: {
                'next_run_time': 1571433194,
                'schedule': {
                    'day': '*',
                    'day_of_week': '*',
                    'hour': '*',
                    'minute': '*',
                    'month': '*',
                    'second': '*/2',
                    'week': '*',
                    'year': '*'
                },
                'status': 'active'
            }
        }

        mock_get_project = self.patch('foundations_contrib.cli.orbit_monitor_package_server.get_by_project', ConditionalReturn())
        mock_get_project.return_when(expected_results, self.project_name, 'scheduler')

        monitors_controller = MonitorsController()
        monitors_controller.params = {'project_name': self.project_name}

        results = monitors_controller.index()
        self.assertEqual(expected_results[self.monitor_id], results[self.monitor_id])

