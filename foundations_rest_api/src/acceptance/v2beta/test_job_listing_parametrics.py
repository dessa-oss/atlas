"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 12 2018
"""
import numpy as np
import foundations
from foundations import create_stage, set_project_name, Hyperparameter
from acceptance.api_acceptance_test_case_base import APIAcceptanceTestCaseBase
from acceptance.v2beta.jobs_tests_helper_mixin_v2 import JobsTestsHelperMixinV2


class TestJobListingParametrics(JobsTestsHelperMixinV2, APIAcceptanceTestCaseBase):
    url = '/api/v2beta/projects/{_project_name}/job_listing'
    sorting_columns = []
    filtering_columns = []

    @classmethod
    def setUpClass(klass):
        JobsTestsHelperMixinV2.setUpClass()
        klass._set_project_name('hanna')
        klass._first_job_name = 'test job 1'
        klass._second_job_name = 'test job 2'
        klass._third_job_name = 'test job 3'
        klass._run_stages()

    @classmethod
    def tearDownClass(klass):
        from foundations_contrib.global_state import redis_connection as redis

        redis.flushall()

    @classmethod
    def _run_stages(klass):

        def make_job(job_name, stage, **kwargs):
            klass._pipeline_context.file_name = job_name
            stage.run_same_process(**kwargs)
            klass._make_completed_job(job_name,  'default user', **kwargs)

        def make_pipeline_context():
            from foundations_internal.pipeline_context import PipelineContext

            klass._pipeline_context = PipelineContext()
            klass._pipeline_context.provenance.project_name = klass._project_name
            klass._pipeline._pipeline_context = klass._pipeline_context

        def stage0(value0):
            return float('nan') if value0 is False else str(value0)

        def stage1(value1, value2):
            return '{} {}'.format(str(value1), str(value2))

        def stage2(value1, value2, value3, value4, dummy_value):
            foundations.log_metric('metric_1', value1)
            foundations.log_metric('metric_2', value2)
            foundations.log_metric('metric_3', value3)
            foundations.log_metric('metric_4', value4)

        def run_first_job():
            make_pipeline_context()
            final_stage = klass._pipeline.stage(stage0, value0=Hyperparameter())
            make_job(klass._first_job_name, final_stage, value0=False)

        def run_second_job():
            make_pipeline_context()
            final_stage = klass._pipeline.stage(
                stage1, 
                value1=Hyperparameter(), 
                value2=Hyperparameter()
            )
            make_job(klass._second_job_name, final_stage, value1=np.nan, value2=37)

        def run_third_job():
            make_pipeline_context()
            input_stage = klass._pipeline.stage(
                stage1, 
                value1=Hyperparameter(), 
                value2=Hyperparameter()
            )
            final_stage = klass._pipeline.stage(
                stage2,
                value1=Hyperparameter(), 
                value2=Hyperparameter(), 
                value3=Hyperparameter(),
                value4=Hyperparameter(),
                dummy_value=input_stage
            )
            make_job(klass._third_job_name, final_stage, value1='hello', value2=True, value3=47.5, value4=np.nan)

        run_first_job()
        run_second_job()
        run_third_job()

    def test_get_route(self):
        data = super(TestJobListingParametrics, self).test_get_route()

        self.assertEqual(data['jobs'][0]['job_id'], self._third_job_name)

        self.assertEqual(data['jobs'][0]['input_params'][0]['name'], 'value1')
        self.assertEqual(data['jobs'][0]['input_params'][1]['name'], 'value2')
        self.assertEqual(data['jobs'][0]['input_params'][2]['name'], 'value2')
        self.assertEqual(data['jobs'][0]['input_params'][3]['name'], 'value3')
        self.assertEqual(data['jobs'][0]['input_params'][4]['name'], 'value4')
        self.assertEqual(data['jobs'][0]['input_params'][5]['name'], 'dummy_value')
        self.assertEqual(data['jobs'][0]['input_params'][0]['value'], 'hello')
        self.assertEqual(data['jobs'][0]['input_params'][1]['value'], True)
        self.assertEqual(data['jobs'][0]['input_params'][2]['value'], 'hello')
        self.assertEqual(data['jobs'][0]['input_params'][3]['value'], True)
        self.assertEqual(data['jobs'][0]['input_params'][4]['value'], 47.5)
        self.assertEqual(data['jobs'][0]['input_params'][5]['value'], None)

        self.assertEqual(data['jobs'][0]['output_metrics'][0]['value'], 'hello')
        self.assertEqual(data['jobs'][0]['output_metrics'][1]['value'], True)
        self.assertEqual(data['jobs'][0]['output_metrics'][2]['value'], 47.5)
        self.assertEqual(data['jobs'][0]['output_metrics'][3]['value'], None)

        self.assertEqual(data['jobs'][1]['job_id'], self._second_job_name)

        self.assertEqual(data['jobs'][1]['input_params'][0]['name'], 'value1')
        self.assertEqual(data['jobs'][1]['input_params'][1]['name'], 'value2')
        self.assertIsNone(data['jobs'][1]['input_params'][0]['value'])

        self.assertEqual(data['jobs'][2]['job_id'], self._first_job_name)

        self.assertEqual(data['jobs'][2]['input_params'][0]['name'], 'value0')
        self.assertFalse(data['jobs'][2]['input_params'][0]['value'])

    def test_filter_bool_true(self):
        query_string = '?metric_2=true'
        custom_method = super(TestJobListingParametrics, self)._get_test_route_method(query_string)
        data = custom_method(self)
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['job_id'], self._third_job_name)

    def test_filter_bool_false(self):
        query_string = '?value0=false'
        custom_method = super(TestJobListingParametrics, self)._get_test_route_method(query_string)
        data = custom_method(self)
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['job_id'], self._first_job_name)

    def test_filter_input_parameter_is_null(self):
        query_string = '?value1_isnull=true'
        custom_method = super(TestJobListingParametrics, self)._get_test_route_method(query_string)
        data = custom_method(self)
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['job_id'], self._second_job_name)

    def test_filter_input_parameter_is_not_null(self):
        query_string = '?value1_isnull=false'
        custom_method = super(TestJobListingParametrics, self)._get_test_route_method(query_string)
        data = custom_method(self)
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['job_id'], self._third_job_name)

    def test_filter_metric_is_null(self):
        query_string = '?metric_4_isnull=true'
        custom_method = super(TestJobListingParametrics, self)._get_test_route_method(query_string)
        data = custom_method(self)
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['job_id'], self._third_job_name)

    def test_filter_metric_is_not_null(self):
        query_string = '?metric_2_isnull=false'
        custom_method = super(TestJobListingParametrics, self)._get_test_route_method(query_string)
        data = custom_method(self)
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['job_id'], self._third_job_name)
