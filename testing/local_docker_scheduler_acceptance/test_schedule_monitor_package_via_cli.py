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
    def _update_scheduled_job(job_name):
        import os
        import requests

        new_schedule = {
            'second': '*/2'
        }

        scheduler_address = os.environ['LOCAL_DOCKER_SCHEDULER_HOST']
        return requests.patch(f'http://{scheduler_address}:5000/scheduled_jobs/{job_name}', json={'schedule': new_schedule})

    @staticmethod
    def _get_scheduled_job(job_name):
        import os
        import requests

        scheduler_address = os.environ['LOCAL_DOCKER_SCHEDULER_HOST']
        return requests.get(f'http://{scheduler_address}:5000/scheduled_jobs/{job_name}')


    @staticmethod
    def _put_to_scheduled_job(job_name, status):
        import os
        import requests

        scheduler_address = os.environ['LOCAL_DOCKER_SCHEDULER_HOST']
        return requests.put(f'http://{scheduler_address}:5000/scheduled_jobs/{job_name}', json={'status': status})

    def _start_monitor(self):
        command = f'python -m foundations monitor create --name={self.monitor_name} --project_name={self.project_name} --env={self.env} {self.monitor_package_dir} main.py '
        return subprocess.run(command.split(), cwd='local_docker_scheduler_acceptance/fixtures/this_cool_monitor/', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def _call_monitor_with_command(self, operation):
        command = f'python -m foundations monitor {operation} --env={self.env} {self.project_name} {self.monitor_name}'
        return subprocess.run(command, shell=True)

    def test_schedule_monitor_package_via_cli_runs_package_code_on_a_schedule(self):
        result = self._start_monitor()
        self.assertEqual(0, result.returncode)
        self.assertIn('Foundations INFO: Job bundle submitted.\n', result.stdout.decode())
        self.assertIn('Foundations INFO: Monitor scheduled.\n', result.stdout.decode())
        self.assertIn(f'Successfully created monitor {self.monitor_name} in project {self.project_name}\n', result.stdout.decode())

        metric_sets = ProductionMetricSet.all(self.project_name).evaluate()
        self.assertEqual([], metric_sets)

        update_response = self._update_scheduled_job(self.monitor_package_id)
        resume_response = self._put_to_scheduled_job(self.monitor_package_id, 'active')
        self.assertEqual(204, update_response.status_code)
        self.assertEqual(204, resume_response.status_code)

        metric_sets = self._wait_for_expected_number_of_runs(1, timeout=30)
        self.assertIn(len(metric_sets[0].series[0]['data']), [2, 3])

        for metric_set in metric_sets:
            self.assertEqual('current_time', metric_set.yAxis['title']['text'])

    def test_schedule_monitor_package_via_cli_with_same_monitor_name_twice_returns_correct_error(self):
        import subprocess

        result = self._start_monitor()
        self.assertEqual(0, result.returncode)

        result = self._start_monitor()
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(f'Unable to create monitor {self.monitor_name} in project {self.project_name}\n', result.stdout.decode())
        self.assertEqual('Command failed with error: Monitor already exists\n', result.stderr.decode())

    def test_schedule_monitor_package_via_cli_with_same_monitor_name_twice_returns_correct_error_when_monitor_name_and_project_name_not_set(self):
        import subprocess

        command = f'python -m foundations monitor create --env={self.env} {self.monitor_package_dir} main.py'
        result = subprocess.run(command.split(), cwd='local_docker_scheduler_acceptance/fixtures/this_cool_monitor/', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(0, result.returncode)

        command = f'python -m foundations monitor create --env={self.env} {self.monitor_package_dir} main.py'
        result = subprocess.run(command.split(), cwd='local_docker_scheduler_acceptance/fixtures/this_cool_monitor/', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(f'Unable to create monitor main-py in project this_cool_monitor\n', result.stdout.decode())
        self.assertEqual('Command failed with error: Monitor already exists\n', result.stderr.decode())

    def test_pause_scheduled_monitor_package_via_cli_halts_execution_but_can_resume_later(self):
        import time

        self._start_monitor()

        self._update_scheduled_job(self.monitor_package_id)
        self._put_to_scheduled_job(self.monitor_package_id, 'active')

        metric_sets_before_pause = self._wait_for_expected_number_of_runs(1, timeout=30)
        before_pause_data_series_length = len(metric_sets_before_pause[0].series[0]['data'])

        pause_result = self._call_monitor_with_command('pause')
        self.assertEqual(0, pause_result.returncode)

        time.sleep(5)
        metric_sets_during_pause = ProductionMetricSet.all(self.project_name).evaluate()
        self.assertEqual(before_pause_data_series_length, len(metric_sets_during_pause[0].series[0]['data']))

        resume_result = self._call_monitor_with_command('resume')
        self.assertEqual(0, resume_result.returncode)
        time.sleep(5)  # monitor scheduled to run every 2 seconds

        metric_sets_after_resume = ProductionMetricSet.all(self.project_name).evaluate()
        data_series_length_after_resume = len(metric_sets_after_resume[0].series[0]['data'])
        self.assertTrue(data_series_length_after_resume > before_pause_data_series_length)

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

    def _wait_for_expected_number_of_runs(self, number_of_runs_lower_bound, timeout=60):
        import time

        metric_sets = []

        for _ in range(timeout):
            metric_sets = ProductionMetricSet.all(self.project_name).evaluate()
            if metric_sets:
                data_length = len(metric_sets[0].series[0]['data'])
                if data_length > number_of_runs_lower_bound:
                    break
            time.sleep(1)

        return metric_sets
