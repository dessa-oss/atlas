
"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

import unittest
from acceptance.v2beta.jobs_tests_helper_mixin_v2 import JobsTestsHelperMixinV2
from acceptance.api_acceptance_test_case_base import APIAcceptanceTestCaseBase


class TestJobsListingUIFriendly(JobsTestsHelperMixinV2, APIAcceptanceTestCaseBase):
    url = '/api/v2beta/projects/{_project_name}/job_listing'
    sorting_columns = []
    filtering_columns = []

    @classmethod
    def setUpClass(klass):
        klass._project_name = 'lou'
        JobsTestsHelperMixinV2.setUpClass()
        klass._make_completed_job_with_metrics('my job 3', 'bach')

    @classmethod
    def tearDownClass(klass):
        from foundations.global_state import redis_connection as redis\

        keys = []
        for name in klass._project_name, 'my job 3':
            keys += redis.keys('*{}*'.format(name))
        redis.delete(*keys)

    @classmethod
    def _prepare_job_input_data(klass):
        from foundations import log_metric

        def callback(arg1, arg2, kwarg1=None, kwarg2=None):
            log_metric('hello', 20)
            return ', '.join([str(arg1), str(arg2), str(kwarg1), str(kwarg2)])
        klass._pipeline.stage(callback, 'life', 42, 'pi', 3.14)

    @classmethod
    def _make_completed_job_with_metrics(klass, job_name, user):
        from foundations_contrib.producers.jobs.queue_job import QueueJob
        from foundations_contrib.producers.jobs.run_job import RunJob
        from foundations_contrib.producers.jobs.complete_job import CompleteJob

        klass._pipeline_context.provenance.project_name = klass._project_name
        klass._pipeline_context.file_name = job_name
        klass._pipeline_context.provenance.user_name = user
        klass._prepare_job_input_data()
        QueueJob(klass._message_router, klass._pipeline_context).push_message()
        RunJob(klass._message_router, klass._pipeline_context).push_message()
        CompleteJob(klass._message_router,
                    klass._pipeline_context).push_message()

    def test_get_route(self):
        data = super(TestJobsListingUIFriendly, self).test_get_route()
        job_data = data['jobs'][0]
        self.assertEqual(len(job_data['input_params']), 4)
        for obj in job_data['input_params']:
            self.assertEqual(len(obj), 4)
        for index, var_name in enumerate(['arg1', 'arg2', 'kwarg1', 'kwarg2']):
            self.assertEqual(job_data['input_params']
                             [index]['name'], var_name + '-0')
        for index, var_type in enumerate(['string', 'number', 'string', 'number']):
            self.assertEqual(job_data['input_params'][index]['type'], var_type)
        for index, var_value in enumerate(['life', 42, 'pi', 3.14]):
            self.assertEqual(job_data['input_params']
                             [index]['value'], var_value)
        for index in range(4):
            self.assertEqual(job_data['input_params']
                             [index]['source'], 'constant')
        input_parameter_names = data['input_parameter_names']
        expected_input_parameter_names = [{'name': 'kwarg2-0', 'type': 'number'},
                                          {'name': 'kwarg1-0', 'type': 'string'},
                                          {'name': 'arg2-0', 'type': 'number'},
                                          {'name': 'arg1-0', 'type': 'string'}]
        self.assertCountEqual(input_parameter_names, expected_input_parameter_names)
