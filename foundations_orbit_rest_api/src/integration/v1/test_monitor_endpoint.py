"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.global_state import app_manager

@skip('not yet implemented')
class TestMonitorEndpoint(Spec):
    
    @let_now
    def project_name(self):
        return self.faker.word()
    
    @let
    def monitor_name(self):
        return self._gen_unique_word()

    @let
    def base_url(self):
        return f'/api/v1/projects/{self.project_name}/monitors'

    client = app_manager.app().test_client()

    def test_pause_monitor_returns_correct_status_code_when_successfull(self):
        self._start_monitor()

        pause_status = self._pause_monitor()
        self.assertEqual(204, pause_status.status_code)

    def test_pause_monitor_halts_monitor_execution(self):
        self._start_monitor()
        self._pause_monitor()

        monitor_id = f'{self.project_name}-{self.monitor_name}'

        from foundations_local_docker_scheduler_plugin.cron_job_scheduler import CronJobScheduler
        from foundations_global import config_manager

        scheduler_url = config_manager.config().get('scheduler_url')
        job_scheduler = CronJobScheduler(scheduler_url)

        results = job_scheduler.get_job(monitor_id)
        self.assertEqual('paused', results['status'])

    def _start_monitor(self):
        payload = {
            'name': self.monitor_name,
            'commands': self.commands,
            'job_directory': self.job_directory_binary
        }

        return self.client.post(self.base_url, json=payload)

    def _get_all_monitors(self):
        return self.client.get(self.base_url)

    def _get_monitors(self, monitor_name=None):
        monitor_name = monitor_name if self.monitor_name is None else monitor_name
        monitor_url = f'{self.base_url}/{monitor_name}'
        return self.client.get(monitor_url)

    def _pause_monitor(self, monitor_name=None):
        payload = {'status': 'pause'}
        monitor_name = monitor_name if self.monitor_name is None else monitor_name
        monitor_url = f'{self.base_url}/{self.monitor_name}'
        return self.client.put(monitor_url, json=payload)

    def _resume_monitor(self, monitor_name=None):
        payload = {'status': 'resume'}
        monitor_name = monitor_name if self.monitor_name is None else monitor_name
        monitor_url = f'{self.base_url}/{self.monitor_name}'
        return self.client.put(monitor_url, json=payload)

    def _delete_monitor(self, monitor_name=None):
        monitor_name = monitor_name if self.monitor_name is None else monitor_name
        monitor_url = f'{self.base_url}/{self.monitor_name}'
        return self.client.delete(monitor_url, json=payload)