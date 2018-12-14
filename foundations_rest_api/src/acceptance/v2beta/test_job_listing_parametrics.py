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
        klass._third_job_name = 'test job 3'
        klass._run_stages()

    @classmethod
    def tearDownClass(klass):
        from foundations.global_state import redis_connection as redis

        keys = []
        for name in (klass._project_name, klass._first_job_name, klass._second_job_name, klass._third_job_name):
            keys += redis.keys('*{}*'.format(name))
        redis.delete(*keys)

    @classmethod
    def _run_stages(klass):

        @create_stage
        def stage0(value0):
            return float('nan') if value0 is False else str(value0)

        @create_stage
        def stage1(value1, value2):
            return '{} {}'.format(str(value1), str(value2))

        @create_stage
        def stage2(value1, value2, value3):
            foundations.log_metric('nan_metric_1', value1)
            foundations.log_metric('nan_metric_2', value2)
            foundations.log_metric('int_metric', value3)

        def run_first_job():
            set_project_name(klass._project_name)
            value1 = stage0(False)
            value2 = stage1(10, 4.5)
            stage2(value1, value2, 5).run(job_name=klass._first_job_name)

        def run_second_job():
            set_project_name(klass._project_name)
            value3 = stage0(None)
            value4 = stage1(np.nan, float('nan'))
            stage2(value3, value4, 8.3).run(job_name=klass._second_job_name)

        def run_third_job():
            set_project_name(klass._project_name)
            value3 = stage0(1)
            value4 = stage1(30, 'some string')
            stage2(value3, value4, 3.14).run(job_name=klass._third_job_name)

        from multiprocessing import Process

        # Fork job run due to bug not allowing Foundation to create more than one job in the same process
        p1 = Process(target=run_first_job)
        p2 = Process(target=run_second_job)
        p3 = Process(target=run_third_job)
        p1.start()
        p1.join()
        p2.start()
        p2.join()
        p3.start()
        p3.join()

    def test_get_route(self):
        data = super(TestJobListingParametrics, self).test_get_route()

        self.assertEqual(data['jobs'][0]['job_id'], self._third_job_name)

        self.assertEqual(data['jobs'][0]['input_params'][0]['name'], 'value0-6')
        self.assertEqual(data['jobs'][0]['input_params'][1]['name'], 'value1-7')
        self.assertEqual(data['jobs'][0]['input_params'][2]['name'], 'value2-7')
        self.assertEqual(data['jobs'][0]['input_params'][3]['name'], 'value1-8')
        self.assertEqual(data['jobs'][0]['input_params'][4]['name'], 'value2-8')
        self.assertEqual(data['jobs'][0]['input_params'][5]['name'], 'value3-8')
        self.assertEqual(data['jobs'][0]['input_params'][0]['value'], 1)
        self.assertEqual(data['jobs'][0]['input_params'][1]['value'], 30)
        self.assertEqual(data['jobs'][0]['input_params'][2]['value'], 'some string')
        self.assertEqual(data['jobs'][0]['input_params'][3]['value'], 'stage0-6')
        self.assertEqual(data['jobs'][0]['input_params'][4]['value'], 'stage1-7')
        self.assertEqual(data['jobs'][0]['input_params'][5]['value'], 3.14)

        self.assertEqual(data['jobs'][0]['output_metrics'][0]['value'], '1')
        self.assertEqual(data['jobs'][0]['output_metrics'][1]['value'], '30 some string')
        self.assertEqual(data['jobs'][0]['output_metrics'][2]['value'], 3.14)

        self.assertEqual(data['jobs'][1]['job_id'], self._second_job_name)

        self.assertEqual(data['jobs'][1]['input_params'][0]['name'], 'value0-3')
        self.assertEqual(data['jobs'][1]['input_params'][1]['name'], 'value1-4')
        self.assertEqual(data['jobs'][1]['input_params'][2]['name'], 'value2-4')
        self.assertEqual(data['jobs'][1]['input_params'][3]['name'], 'value1-5')
        self.assertEqual(data['jobs'][1]['input_params'][4]['name'], 'value2-5')
        self.assertEqual(data['jobs'][1]['input_params'][5]['name'], 'value3-5')
        # This "NoneType" must be changed to None when bug is addressed in FOUND-715
        self.assertEqual(data['jobs'][1]['input_params'][0]['value'], 'NoneType')
        self.assertIsNone(data['jobs'][1]['input_params'][1]['value'])
        self.assertIsNone(data['jobs'][1]['input_params'][2]['value'])
        self.assertEqual(data['jobs'][1]['input_params'][3]['value'], 'stage0-3')
        self.assertEqual(data['jobs'][1]['input_params'][4]['value'], 'stage1-4')
        self.assertEqual(data['jobs'][1]['input_params'][5]['value'], 8.3)

        self.assertEqual(data['jobs'][1]['output_metrics'][0]['value'], 'None')
        self.assertEqual(data['jobs'][1]['output_metrics'][1]['value'], 'nan nan')
        self.assertEqual(data['jobs'][1]['output_metrics'][2]['value'], 8.3)

        self.assertEqual(data['jobs'][2]['job_id'], self._first_job_name)

        self.assertEqual(data['jobs'][2]['input_params'][0]['name'], 'value0-0')
        self.assertEqual(data['jobs'][2]['input_params'][1]['name'], 'value1-1')
        self.assertEqual(data['jobs'][2]['input_params'][2]['name'], 'value2-1')
        self.assertEqual(data['jobs'][2]['input_params'][3]['name'], 'value1-2')
        self.assertEqual(data['jobs'][2]['input_params'][4]['name'], 'value2-2')
        self.assertEqual(data['jobs'][2]['input_params'][5]['name'], 'value3-2')
        self.assertEqual(data['jobs'][2]['input_params'][0]['value'], False)
        self.assertEqual(data['jobs'][2]['input_params'][1]['value'], 10)
        self.assertEqual(data['jobs'][2]['input_params'][2]['value'], 4.5)
        self.assertEqual(data['jobs'][2]['input_params'][3]['value'], 'stage0-0')
        self.assertEqual(data['jobs'][2]['input_params'][4]['value'], 'stage1-1')
        self.assertEqual(data['jobs'][2]['input_params'][5]['value'], 5)

        self.assertIsNone(data['jobs'][2]['output_metrics'][0]['value'])
        self.assertEqual(data['jobs'][2]['output_metrics'][1]['value'], '10 4.5')
        self.assertEqual(data['jobs'][2]['output_metrics'][2]['value'], 5)
