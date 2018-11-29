"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

import unittest
from acceptance.v2beta.jobs_tests_helper_mixin import JobsTestsHelperMixin
from acceptance.api_acceptance_test_case_base import APIAcceptanceTestCaseBase


class TestJobsListingEndpointV2(JobsTestsHelperMixin, APIAcceptanceTestCaseBase):
    url = '/api/v2beta/projects/{_project_name}/job_listing'
    sorting_columns = ['start_time', 'status']

    @classmethod
    def setUpClass(klass):
        klass._project_name = 'hana'
        JobsTestsHelperMixin.setUpClass()
        klass._setup_three_jobs()

    @classmethod
    def tearDownClass(klass):
        from foundations.global_state import redis_connection as redis
        keys = []
        for name in klass._project_name, '00000000-0000-0000-0000-000000000000', 'my job 1', 'my job 2':
            keys += redis.keys('*{}*'.format(name))
        redis.delete(*keys)

    @classmethod
    def _setup_three_jobs(klass):
        from time import sleep
        klass._pipeline_context.provenance.project_name = klass._project_name
        klass._make_running_job('00000000-0000-0000-0000-000000000000', 'soju hero')
        sleep(0.01)
        klass._make_completed_job('my job 1', 'beethoven')
        sleep(0.01)
        klass._make_completed_job('my job 2', 'mozart')

    def test_get_route(self):
        data = super(TestJobsListingEndpointV2, self).test_get_route()
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_route_sorted_start_time_descending(self):
        data = super(TestJobsListingEndpointV2, self).test_route_sorted_start_time_descending()
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_route_sorted_start_time_ascending(self):
        data = super(TestJobsListingEndpointV2, self).test_route_sorted_start_time_ascending()
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 2')

    def test_route_sorted_status_descending(self):
        data = super(TestJobsListingEndpointV2, self).test_route_sorted_status_descending()
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 1')

    def test_route_sorted_status_ascending(self):
        data = super(TestJobsListingEndpointV2, self).test_route_sorted_status_ascending()
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_get_route_all_ascending(self):
        data = super(TestJobsListingEndpointV2, self).test_get_route_all_ascending()
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 2')

    def test_get_route_all_descending(self):
        data = super(TestJobsListingEndpointV2, self).test_get_route_all_descending()
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_get_route_alternation(self):
        data = super(TestJobsListingEndpointV2, self).test_get_route_alternation()
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 2')
