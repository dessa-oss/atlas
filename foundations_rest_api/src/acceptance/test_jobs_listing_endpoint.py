"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

import unittest
import json
from foundations_rest_api.global_state import app_manager
from test.v1.models.jobs_tests_helper_mixin import JobsTestsHelperMixin
from .api_acceptance_test_case_base import APIAcceptanceTestCaseBase


class TestJobsListingEndpoint(JobsTestsHelperMixin, APIAcceptanceTestCaseBase):
    url = '/api/v1/projects/{_project_name}/job_listing'
    sorting_columns = ['start_time', 'status']

    def setUp(self):
        self._setup_deployment('RUNNING')
        self._setup_results_archiving()
        self._project_name = 'hana'
        self._setup_two_jobs()

    def tearDown(self):
        self._cleanup()

    def _setup_two_jobs(self):
        def method():
            from foundations.stage_logging import log_metric
            log_metric('loss', 15.33)

        stage = self._pipeline.stage(method)
        self._pipeline_context.provenance.project_name = self._project_name
        self._make_running_job('00000000-0000-0000-0000-000000000000', 123456789, 9999, 'soju hero')
        self._make_completed_job('my job 1', stage, 123456789, 9999999999)
        self._make_completed_job('my job 2', stage, 9999999999, 9999999999)

    def test_get_route(self):        
        data = super(TestJobsListingEndpoint, self).test_get_route()
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][1]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 1')

    def test_route_sorted_start_time_descending(self):
        data = super(TestJobsListingEndpoint, self).test_route_sorted_start_time_descending()
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][1]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 1')

    def test_route_sorted_start_time_ascending(self):
        data = super(TestJobsListingEndpoint, self).test_route_sorted_start_time_ascending()
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 2')

    def test_route_sorted_status_descending(self):
        data = super(TestJobsListingEndpoint, self).test_route_sorted_status_descending()
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 1')

    def test_route_sorted_status_ascending(self):
        data = super(TestJobsListingEndpoint, self).test_route_sorted_status_ascending()
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_get_route_all_ascending(self):
        data = super(TestJobsListingEndpoint, self).test_get_route_all_ascending()
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][1]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 2')

    def test_get_route_all_descending(self):
        data = super(TestJobsListingEndpoint, self).test_get_route_all_descending()
        self.assertEqual(data['jobs'][0]['job_id'], 'my job 2')
        self.assertEqual(data['jobs'][1]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 1')
        
    def test_get_route_alternation(self):
        data = super(TestJobsListingEndpoint, self).test_get_route_alternation()
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job 1')
        self.assertEqual(data['jobs'][2]['job_id'], 'my job 2')
