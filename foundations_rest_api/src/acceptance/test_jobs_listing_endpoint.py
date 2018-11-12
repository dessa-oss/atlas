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
    url = '/api/v1/projects/default/job_listing'
    sorting_columns = ['start_time']

    def setUp(self):
        self._setup_deployment('RUNNING')
        self._setup_results_archiving()
        self._setup_two_jobs()

    def tearDown(self):
        self._cleanup()

    def _setup_two_jobs(self):
        def method():
            from foundations.stage_logging import log_metric
            log_metric('loss', 15.33)

        stage = self._pipeline.stage(method)
        self._make_completed_job('my job', stage, 9999999999, 9999999999)
        self._make_running_job('00000000-0000-0000-0000-000000000000', 123456789, 9999, 'soju hero')

    def test_get_route(self):        
        data = super(TestJobsListingEndpoint, self).test_get_route()
        self.assertEqual(data['jobs'][0]['job_id'], 'my job')
        self.assertEqual(data['jobs'][1]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_get_route_with_start_time_sorted_descendant(self):
        data = super(TestJobsListingEndpoint, self).test_get_route_with_start_time_sorted_descendant()
        self.assertEqual(data['jobs'][0]['job_id'], 'my job')
        self.assertEqual(data['jobs'][1]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_get_route_with_start_time_sorted_ascendant(self):
        data = super(TestJobsListingEndpoint, self).test_get_route_with_start_time_sorted_ascendant()
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job')
