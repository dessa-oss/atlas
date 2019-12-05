"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from foundations_spec import *
from foundations_orbit import DataContract


# TODO !!!! Note that the validate will fail in dataframe is created with 100 records
class TestDataContractWithMonitor(Spec):

    @let
    def reference_dataframe_with_10_rows(self):
        import pandas
        return pandas.DataFrame(self._create_rows(10))

    @let
    def contract_name(self):
        return 'test_data_contract_with_monitor'

    @let
    def inference_period(self):
        return '2019-10-31'

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def monitor_name(self):
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
    def project_dir(self):
        return './orbit_acceptance/fixtures/contract_for_monitor'

    @let
    def reference_dataframe_nans(self):
        import pandas, numpy
        dataframe = pandas.DataFrame(self._create_rows(1000))
        return dataframe.mask(numpy.random.random(dataframe.shape) < .1)

    @set_up
    def set_up(self):
        from foundations_contrib.global_state import redis_connection
        redis_connection.flushall()

    @tear_down
    def tear_down(self):
        import os
        try:
            os.remove(f'{self.project_dir}/reference_data.pkl')
            os.remove(f'{self.project_dir}/test_data_contract_with_monitor.pkl')
        except:
            pass

        self._delete_scheduled_job(self.monitor_package_id)

    @staticmethod
    def _delete_scheduled_job(job_name):
        import os
        import requests

        scheduler_address = os.environ['LOCAL_DOCKER_SCHEDULER_HOST']
        return requests.delete(f'http://{scheduler_address}:5000/scheduled_jobs/{job_name}')

    def _start_monitor(self):
        import subprocess
        command = f'python -m foundations monitor create --name={self.monitor_name} --project_name={self.project_name} --env={self.env} {self.monitor_package_dir} validate.py '
        return subprocess.run(command.split(), cwd=self.project_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def _create_rows(self, num=1):
        import numpy
        random_words = [self.faker.word() for _ in range(5)]
        output = [
            {
                "cat_string": numpy.random.choice(random_words),
                "string": self.faker.word(),
                "date_time": self.faker.date_time(),
                "booleans": self.faker.pybool(),
                "cat_int": numpy.random.choice([1, 2, 3, 4, 5]),
                "integers": self.faker.pyint(),
                "floats": self.faker.pyint() / 17
            }
            for x in range(num)
        ]

        return output

    def test_data_contract_with_monitor_using_smaller_dataset(self):
        contract = DataContract(self.contract_name, self.reference_dataframe_with_10_rows)
        contract.save(self.project_dir)
        self.reference_dataframe_with_10_rows.to_pickle(f'{self.project_dir}/reference_data.pkl')

        result = self._start_monitor()
        self.assertEqual(0, result.returncode)

        validation_results = self._wait_for_validation_result(180)

        self._assert_validation_results_has_correct_structure(validation_results)

    def _assert_validation_results_has_correct_structure(self, validation_results):
        for key in ['data_quality', 'max', 'min', 'population_shift', 'row_count', 'schema']:
            self.assertIn(key, validation_results.keys())

        self.assertTrue(self.monitor_package_id in validation_results['job_id'])

    def _get_validation_reports(self):
        from foundations_orbit_rest_api.v1.controllers.validation_reports_controller import ValidationReportsController
        controller = ValidationReportsController()
        controller.params = {
            'inference_period': self.inference_period,
            'monitor_package': self.monitor_name,
            'data_contract': self.contract_name,
            'project_name': self.project_name,
        }
        return controller.post().as_json()

    def _wait_for_validation_result(self, timeout=60):
        import time

        validation_reports = {}

        for _ in range(timeout):
            validation_reports = self._get_validation_reports()
            if 'error' not in validation_reports:
                break
            time.sleep(1)

        return validation_reports
