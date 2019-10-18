"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 10 2019
"""

from foundations_spec import *
from foundations_monitor_rest_api.v1.controllers.monitor_controller import MonitorController

@skip('Work in progress')
class TestMonitorController(Spec):

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
    
    def test_request_for_monitors_with_project_returns_monitors(self):
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
        
        self.cron_job_scheduler.get_job_with_params.return_when(expected_results, {'job_id_prefix': self.project_name})

        monitor_controller = MonitorController()
        monitor_controller.params = {'project_name': self.project_name}

        results = monitor_controller.index()
        self.assertEqual(expected_results[self.monitor_id], results[self.monitor_id])

