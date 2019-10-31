"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from foundations_spec import *
from foundations_orbit import DataContract

import orbit_acceptance.config # Set up foundations environment

class TestDataContractWithMonitor(Spec):

    @let
    def reference_dataframe(self):
        import pandas
        return pandas.DataFrame(self._create_rows(100))

    @let
    def contract_name(self):
        return 'test_data_contract_with_monitor'

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

    @set_up
    def set_up(self):
        import os
        from foundations_contrib.global_state import redis_connection

        redis_connection.flushall()

    @tear_down
    def tear_down(self):
        import os
        os.remove('./orbit_acceptance/fixtures/end-to-end-acceptance/project/reference_data.pkl')
        os.remove('./orbit_acceptance/fixtures/end-to-end-acceptance/project/test_data_contract_with_monitor.pkl')

        self._delete_scheduled_job(self.monitor_package_id)

    @staticmethod
    def _delete_scheduled_job(job_name):
        import os
        import requests
        
        scheduler_address = os.environ['LOCAL_DOCKER_SCHEDULER_HOST']
        return requests.delete(f'http://{scheduler_address}:5000/scheduled_jobs/{job_name}')

    def _start_monitor(self):
        import subprocess

        import os

        command = f'python -m foundations monitor create --name={self.monitor_name} --project_name={self.project_name} --env={self.env} {self.monitor_package_dir} validate.py '
        return subprocess.run(command.split(), cwd='orbit_acceptance/fixtures/end-to-end-acceptance/project/', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 
    @let
    def reference_dataframe_nans(self):
        import pandas, numpy
        dataframe = pandas.DataFrame(self._create_rows(1000))
        return dataframe.mask(numpy.random.random(dataframe.shape) < .1)

    def _create_rows(self, num=1):
        import numpy
        random_words = [self.faker.word() for _ in range(5)]
        output = [
            {
                "cat_string":numpy.random.choice(random_words),
                "string":self.faker.word(),
                "date_time":self.faker.date_time(),
                "booleans":self.faker.pybool(),
                "cat_int":numpy.random.choice([1,2,3,4,5]),
                "integers":self.faker.pyint(),
                "floats":self.faker.pyint()/17
            } 
            for x in range(num)]
                
        return output

    def test_data_contract_with_monitor(self):
        contract = DataContract(self.contract_name, self.reference_dataframe)
        contract.save('./orbit_acceptance/fixtures/end-to-end-acceptance/project')

        self.reference_dataframe.to_pickle('./orbit_acceptance/fixtures/end-to-end-acceptance/project/reference_data.pkl')

        result = self._start_monitor()
        self.assertEqual(0, result.returncode)

        validation_results = self._wait_for_expected_number_of_runs(1)

        self._assert_validation_results_has_correct_structure(validation_results)

    def _assert_validation_results_has_correct_structure(self, validation_results):
        for key in ['data_quality', 'max', 'min', 'population_shift', 'row_count', 'schema']:
            self.assertIn(key, validation_results.keys())
        
        self.assertTrue(self.monitor_package_id in validation_results['job_id'])

    def _wait_for_expected_number_of_runs(self, number_of_runs_lower_bound, timeout=60):
        from foundations_contrib.global_state import redis_connection
        import time
        import pickle
        
        validation_reports = []
        for _ in range(timeout):
            validation_reports = redis_connection.keys(f'projects:{self.project_name}:monitors:{self.monitor_name}:validation:{self.contract_name}')
            if validation_reports:
                if len(validation_reports) >= number_of_runs_lower_bound:
                    break
            time.sleep(1)

        encoded_redis_results = redis_connection.hget(validation_reports[0], '2019-10-31')
        decoded_redis_results = pickle.loads(encoded_redis_results)

        return decoded_redis_results 