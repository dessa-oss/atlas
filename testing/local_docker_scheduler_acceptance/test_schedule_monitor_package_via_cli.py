"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

import subprocess
from foundations_orbit_rest_api.v1.models.production_metric_set import ProductionMetricSet

@skip('Not implemented')
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
        return 'local_docker_scheduler_acceptance/fixtures/this_cool_monitor'

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

    def _start_monitor(self):
        command = (f'python -m foundations monitor start {self.monitor_package_dir} main.py '
                   f'--name={self.monitor_name} --project_name={self.project_name} --env={self.env}')
        return subprocess.run(command, shell=True)

    def _call_monitor_with_command(self, operation):
        command = f'python -m foundations monitor {operation} {self.monitor_name} {self.project_name} --env={self.env}'
        return subprocess.run(command, shell=True)

    def test_schedule_monitor_package_via_cli_runs_package_code_on_a_schedule(self):
        import time
        
        result = self._start_monitor()

        self.assertEqual(0, result.returncode)

        time.sleep(7)

        response = self._delete_scheduled_job(self.monitor_package_id)
        self.assertEqual(204, response.status_code)

        metric_sets = ProductionMetricSet.all(self.project_name).evaluate()

        self.assertIn(len(metric_sets), [3, 4])

        for metric_set in metric_sets:
            self.assertEqual('current_time', metric_set.yAxis['title']['text'])
            print(metric_set.series)

    def test_pause_scheduled_monitor_package_via_cli_halts_execution_but_can_resume_later(self):
        import time

        result = self._start_monitor()

        pause_result = subprocess.run(
            [
                'python', '-m',
                'foundations', 'orbit', 'monitor', 'pause',
                f'--monitor={self.monitor_name}',
                f'--project_name={self.project_name}'
            ]
        )

        self.assertEqual(0, pause_result.returncode)

        time.sleep(7)
        metric_sets_before_resume = ProductionMetricSet.all(self.project_name).evaluate()
        self.assertIn(len(metric_sets_before_resume), [0, 1])

        resume_result = self._call_monitor_with_command('resume')

        self.assertEqual(0, resume_result.returncode)

        time.sleep(7)
        metric_sets_after_resume = ProductionMetricSet.all(self.project_name).evaluate()
        self.assertIn(len(metric_sets_after_resume), [3, 4, 5])