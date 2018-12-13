"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 12 2018
"""
import numpy as np
import foundations
from foundations import create_stage, set_project_name
from acceptance.api_acceptance_test_case_base import APIAcceptanceTestCaseBase


class TestJobListingParametrics(APIAcceptanceTestCaseBase):
    url = '/api/v2beta/projects/{_project_name}/job_listing'
    sorting_columns = []
    filtering_columns = []

    @classmethod
    def setUpClass(klass):
        klass._project_name = 'hanna'
        klass._first_job_name = 'test job 1'
        klass._second_job_name = 'test job 2'
        klass._run_stages()

    @classmethod
    def tearDownClass(klass):
        from foundations.global_state import redis_connection as redis

        keys = []
        for name in (klass._project_name, klass._first_job_name, klass._second_job_name):
            keys += redis.keys('*{}*'.format(name))
        redis.delete(*keys)

    @classmethod
    def _run_stages(klass):

        @create_stage
        def stage0():
            return float('nan')

        @create_stage
        def stage1(value1, value2):
            return np.nan

        @create_stage
        def stage2(value1, value2, value3):
            foundations.log_metric('nan_metric_1', value1)
            foundations.log_metric('nan_metric_2', value2)
            foundations.log_metric('int_metric', value3)

        def run_first_job():
            set_project_name(klass._project_name)
            value1 = stage0()
            value2 = stage1(10, None)
            stage2(value1, value2, 5).run(job_name=klass._first_job_name)

        def run_second_job():
            set_project_name(klass._project_name)
            value3 = stage0()
            value4 = stage1(20, float('nan'))
            stage2(value3, value4, 8.3).run(job_name=klass._second_job_name)

        from multiprocessing import Process

        p = Process(target=run_first_job)
        p.start()
        p.join()
        p = Process(target=run_second_job)
        p.start()
        p.join()

    def test_get_route(self):
        data = super(TestJobListingParametrics, self).test_get_route()
        self.assertEqual(data['jobs'][0]['job_id'], self._second_job_name)
        self.assertEqual(data['jobs'][0]['input_params'][0]['value'], 20)
        self.assertEqual(data['jobs'][0]['input_params'][1]['value'], None)
        self.assertEqual(data['jobs'][0]['input_params'][2]['value'], 'stage0-2')
        self.assertEqual(data['jobs'][0]['input_params'][3]['value'], 'stage1-3')
        self.assertEqual(data['jobs'][0]['input_params'][4]['value'], 8.3)

        self.assertIsNone(data['jobs'][0]['output_metrics'][0]['value'])
        self.assertIsNone(data['jobs'][0]['output_metrics'][1]['value'])
        self.assertEqual(data['jobs'][0]['output_metrics'][2]['value'], 8.3)

        self.assertEqual(data['jobs'][1]['job_id'], self._first_job_name)
        self.assertEqual(data['jobs'][1]['input_params'][0]['value'], 10)
        # This "NoneType" must be changed to None when bug is addressed in FOUND-715
        self.assertEqual(data['jobs'][1]['input_params'][1]['value'], 'NoneType')
        self.assertEqual(data['jobs'][1]['input_params'][2]['value'], 'stage0-2')
        self.assertEqual(data['jobs'][1]['input_params'][3]['value'], 'stage1-0')
        self.assertEqual(data['jobs'][1]['input_params'][4]['value'], 5)

        self.assertIsNone(data['jobs'][1]['output_metrics'][0]['value'])
        self.assertIsNone(data['jobs'][1]['output_metrics'][1]['value'])
        self.assertEqual(data['jobs'][1]['output_metrics'][2]['value'], 5)
