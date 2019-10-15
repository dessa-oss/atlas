"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

import subprocess
from foundations_orbit_rest_api.v1.models.production_metric_set import ProductionMetricSet

@skip
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
    def foundations_home(self):
        import os
        return os.environ['FOUNDATIONS_HOME']

    @staticmethod
    def _delete_scheduled_job(job_name):
        import os
        import requests
        
        scheduler_address = os.environ['LOCAL_DOCKER_SCHEDULER_HOST']
        return requests.delete(f'http://{scheduler_address}:5000/scheduled_jobs/{job_name}')

    def test_schedule_monitor_package_via_cli_runs_package_code_on_a_schedule(self):
        import time
        
        result = subprocess.run(
            [
                'foundations', 'orbit', 'monitor', 'start',
                f'--monitor={self.monitor_name}',
                f'--project_name={self.project_name}',
                f'--job_directory={self.monitor_package_dir}'
            ]
        )

        self.assertEqual(0, result.returncode)

        time.sleep(7)

        response = self._delete_scheduled_job(self.monitor_package_id)
        self.assertEqual(204, response.status_code)

        metric_sets = ProductionMetricSet.all(self.project_name).evaluate()

        self.assertIn(len(metric_sets), [3, 4])

        for metric_set in metric_sets:
            self.assertEqual('current_time', metric_set.yAxis['title']['text'])
            print(metric_set.series)