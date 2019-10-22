"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 10 2019
"""

from foundations_spec import *

from foundations_orbit_rest_api.global_state import app_manager


class TestScheduledMonitorEndpoint(Spec):
    
    @let_now
    def project_name(self):
        return self.faker.word()
    
    @let
    def monitor_name(self):
        return self.faker.word()

    @let
    def monitor_id(self):
        return f'{self.project_name}-{self.monitor_name}'

    @let
    def base_url(self):
        return f'/api/v1/projects/{self.project_name}/monitors'

    @let
    def cron_job_scheduler(self):
        from foundations_local_docker_scheduler_plugin.cron_job_scheduler import CronJobScheduler
        from foundations_contrib.global_state import config_manager
        scheduler_url = config_manager.config().get('scheduler_url')
        return CronJobScheduler(scheduler_url)

    client = app_manager.app().test_client()

    @tear_down
    def tear_down(self):
        try:
            self._delete_monitor_via_orbit_monitor_package()
            # print(f'monitor: {self.project_name}-{self.monitor_name}')
        except Exception as e:
            print(f'failed to stop monitor with id: {self.project_name}-{self.monitor_name} with reason: {e}')

    @skip('work in progress implemented')
    def test_pause_monitor_returns_correct_status_code_when_successful(self):
        self._start_monitor()

        pause_status = self._pause_monitor()
        self.assertEqual(204, pause_status.status_code)

    def test_get_request_retrieves_monitors(self):
        self._start_monitor()
        monitor = self._get_monitor()
        self.assertEqual(1, len(monitor.keys()))
        self.assertIsNotNone(monitor[self.monitor_id])

    def test_get_request_by_monitor_id_retrieves_specific_monitor(self):
        self._start_monitor()
        monitors = self._get_all_monitors()
        self.assertTrue(self.monitor_id in monitors.keys())


    @skip('not implemented')
    def test_pause_monitor_halts_monitor_execution(self):
        self._start_monitor()
        self._pause_monitor()

        results = self.cron_job_scheduler.get_job(self.monitor_id)
        self.assertEqual('paused', results['status'])

    def _start_monitor(self):
        from foundations_contrib.cli.orbit_monitor_package_server import start
        import os

        self.set_foundations_home()

        job_directory = os.path.abspath('integration/fixtures/monitor_job')
        command = ['main.py']

        start(job_directory, command, self.project_name, self.monitor_name, 'scheduler')
        self.cron_job_scheduler.update_job_schedule(self.monitor_id, {'second': '*/2'})
        self.cron_job_scheduler.resume_job(self.monitor_id)

    def _delete_monitor_via_orbit_monitor_package(self):
        from foundations_contrib.cli.orbit_monitor_package_server import delete
        delete(self.project_name, self.monitor_name)

    @staticmethod
    def set_foundations_home():
        import os
        os.environ['FOUNDATIONS_HOME'] = os.path.abspath('../../testing/local_docker_scheduler_acceptance/foundations_home')
        os.environ['FOUNDATIONS_COMMAND_LINE'] = 'True'

    def _get_all_monitors(self):
        import json
        response = self.client.get(self.base_url)
        response_data = response.data.decode()
        return json.loads(response_data)

    def _get_monitor(self, monitor_name=None):
        import json
        monitor_name = self.monitor_name if monitor_name is None else monitor_name
        monitor_url = f'{self.base_url}/{monitor_name}'
        response =  self.client.get(monitor_url)
        response_data = response.data.decode()
        return json.loads(response_data)

    def _pause_monitor(self, monitor_name=None):
        payload = {'status': 'pause'}
        monitor_name = self.monitor_name if monitor_name is None else monitor_name
        monitor_url = f'{self.base_url}/{monitor_name}'

        # print(f'URL: {monitor_url}, payload: {payload}')
        return self.client.put(monitor_url, json=payload)

    def _resume_monitor(self, monitor_name=None):
        payload = {'status': 'resume'}
        monitor_name = self.monitor_name if monitor_name is None else monitor_name
        monitor_url = f'{self.base_url}/{monitor_name}'
        return self.client.put(monitor_url, json=payload)

    def _delete_monitor(self, monitor_name=None):
        monitor_name = self.monitor_name if monitor_name is None else monitor_name
        monitor_url = f'{self.base_url}/{monitor_name}'
        return self.client.delete(monitor_url)