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
    filtering_columns = [{'name': 'job_id',
                          'test_values': ('00000000-0000-0000-0000-000000000000', 'my job 1')},
                         {'name': 'status',
                          'test_values': ('queued', 'running')},
                         {'name': 'user',
                          'test_values': ('beethoven', 'soju hero')}
                        ]

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

    def test_sorted_start_time_descending(self):
        data = super(TestJobsListingEndpointV2, self).test_sorted_start_time_descending()
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_sorted_start_time_ascending(self):
        data = super(TestJobsListingEndpointV2, self).test_sorted_start_time_ascending()
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 2')

    def test_sorted_status_descending(self):
        data = super(TestJobsListingEndpointV2, self).test_sorted_status_descending()
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 1')

    def test_sorted_status_ascending(self):
        data = super(TestJobsListingEndpointV2, self).test_sorted_status_ascending()
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_all_ascending(self):
        data = super(TestJobsListingEndpointV2, self).test_all_ascending()
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 2')

    def test_all_descending(self):
        data = super(TestJobsListingEndpointV2, self).test_all_descending()
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_alternation(self):
        data = super(TestJobsListingEndpointV2, self).test_alternation()
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 2')

    def test_filter_job_id_range(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_job_id_range()
        self.assertEqual(len(data['jobs']), 2)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][1]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_filter_job_id_exact_match_one_option(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_job_id_exact_match_one_option()
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_filter_job_id_exact_match_two_options(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_job_id_exact_match_two_options()
        self.assertEqual(len(data['jobs']), 2)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][1]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_filter_status_range(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_status_range()
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_filter_status_exact_match_one_option(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_status_exact_match_one_option()
        self.assertEqual(len(data['jobs']), 0)

    def test_filter_status_exact_match_two_options(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_status_exact_match_two_options()
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_filter_user_range(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_user_range()
        self.assertEqual(len(data['jobs']), 3)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_filter_user_exact_match_one_option(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_user_exact_match_one_option()
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 1')

    def test_filter_user_exact_match_two_options(self):
        data = super(TestJobsListingEndpointV2, self).test_filter_user_exact_match_two_options()
        self.assertEqual(len(data['jobs']), 2)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][1]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_filter_job_id_contains(self):
        custom_test_method = super(TestJobsListingEndpointV2, self)._get_test_route_method('?job_id_contains=1')
        data = custom_test_method(self)
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 1')

    def test_filter_user_contains(self):
        custom_test_method = super(TestJobsListingEndpointV2, self)._get_test_route_method('?user_contains=hero')
        data = custom_test_method(self)
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')
