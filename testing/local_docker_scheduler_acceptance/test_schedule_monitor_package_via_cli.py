"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

import subprocess
from foundations_orbit_rest_api.v1.models.production_metric_set import ProductionMetricSet

class TestScheduleMonitorPackageViaCli(Spec):
    
    @let
    def monitor_name(self):
        return self.faker.word()

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def monitor_package_id(self):
        return f'{self.project_name}-{self.monitor_name}'

    @let
    def monitor_package_dir(self):
        return '.'

    @let
    def env(self):
        return 'scheduler'

    @let
    def foundations_home(self):
        import os
        return os.environ['FOUNDATIONS_HOME']

    @set_up
    def set_up(self):
        from foundations_contrib.global_state import redis_connection
        redis_connection.flushall()

    @tear_down
    def tear_down(self):
        self._delete_scheduled_job(self.monitor_package_id)

    @staticmethod
    def _delete_scheduled_job(job_name):
        import os
        import requests
        
        scheduler_address = os.environ['LOCAL_DOCKER_SCHEDULER_HOST']
        return requests.delete(f'http://{scheduler_address}:5000/scheduled_jobs/{job_name}')

    @staticmethod
    def _get_scheduled_job(job_name):
        import os
        import requests

        scheduler_address = os.environ['LOCAL_DOCKER_SCHEDULER_HOST']
        return requests.get(f'http://{scheduler_address}:5000/scheduled_jobs/{job_name}')

    def _start_monitor(self):
        import os

        command = f'python -m foundations monitor start --name={self.monitor_name} --project_name={self.project_name} --env={self.env} {self.monitor_package_dir} main.py '
        return subprocess.run(command.split(), cwd='local_docker_scheduler_acceptance/fixtures/this_cool_monitor/')

    def _call_monitor_with_command(self, operation):
        command = f'python -m foundations monitor {operation} --env={self.env} {self.project_name} {self.monitor_name}'
        return subprocess.run(command, shell=True)

    def test_schedule_monitor_package_via_cli_runs_package_code_on_a_schedule(self):
        import time
        
        result = self._start_monitor()

        self.assertEqual(0, result.returncode)

        metric_sets = []
        data_length = 0
        for _ in range(60):
            metric_sets = ProductionMetricSet.all(self.project_name).evaluate()
            if metric_sets:
                data_length = len(metric_sets[0].series[0]['data'])
                if data_length >= 3:
                    break
            time.sleep(1)

        response = self._delete_scheduled_job(self.monitor_package_id)
        self.assertEqual(204, response.status_code)

        self.assertGreaterEqual(data_length, 3)

        for metric_set in metric_sets:
            self.assertEqual('current_time', metric_set.yAxis['title']['text'])

    def test_pause_scheduled_monitor_package_via_cli_halts_execution_but_can_resume_later(self):
        import time

        result = self._start_monitor()
        time.sleep(3)

        pause_result = self._call_monitor_with_command('pause')
        
        self.assertEqual(0, pause_result.returncode)

        time.sleep(7)

        metric_sets_before_resume = []
        data_length = 0
        for _ in range(60):
            metric_sets_before_resume = ProductionMetricSet.all(self.project_name).evaluate()
            if metric_sets_before_resume:
                data_length = len(metric_sets_before_resume[0].series[0]['data'])
                if data_length > 0:
                    break
            time.sleep(1)

        self.assertEqual(1, len(metric_sets_before_resume[0].series[0]['data']))

        resume_result = self._call_monitor_with_command('resume')

        self.assertEqual(0, resume_result.returncode)

        metric_sets_after_resume = []
        data_length = 0
        for _ in range(60):
            metric_sets_after_resume = ProductionMetricSet.all(self.project_name).evaluate()
            if metric_sets_after_resume:
                data_length = len(metric_sets_after_resume[0].series[0]['data'])
                if data_length >= 3:
                    break
            time.sleep(1)

        time.sleep(7)

        metric_sets_after_resume = ProductionMetricSet.all(self.project_name).evaluate()
        self.assertIn(len(metric_sets_after_resume[0].series[0]['data']), [3, 4, 5])

    def test_delete_scheduled_monitor_package_removes_cron_job(self):
        import time

        self._start_monitor()
        time.sleep(2)

        get_job_response = self._get_scheduled_job(self.monitor_package_id)
        self.assertIn(self.monitor_package_id, get_job_response.json())

        delete_result = self._call_monitor_with_command('delete')
        self.assertEqual(0, delete_result.returncode)
        time.sleep(2)

        get_job_response = self._get_scheduled_job(self.monitor_package_id)
        self.assertEqual(404, get_job_response.status_code)
        self.assertEqual(f'Scheduled job {self.monitor_package_id} not found', get_job_response.text)