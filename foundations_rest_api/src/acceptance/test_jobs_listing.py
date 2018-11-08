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


class TestJobsListing(unittest.TestCase, JobsTestsHelperMixin):

    def setUp(self):
        self.client = app_manager.app().test_client(self)
        self._setup_deployment('RUNNING')
        self._setup_results_archiving()

        def method():
            from foundations.stage_logging import log_metric
            log_metric('loss', 15.33)

        stage = self._pipeline.stage(method)
        self._make_completed_job('my job', stage, 9999999999, 9999999999)
        self._make_running_job('00000000-0000-0000-0000-000000000000', 123456789, 9999, 'soju hero')

    def tearDown(self):
        self._cleanup()

    def test_get_jobs_listing(self):        
        url = '/api/v1/projects/{}/job_listing'
        resp = self.client.get(url.format('default'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job')
        self.assertEqual(data['jobs'][1]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_get_jobs_listing_sorted_by_start_date_descendant(self):
        url = '/api/v1/projects/{}/job_listing?sort=-start_time'
        resp = self.client.get(url.format('default'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['jobs'][0]['job_id'], 'my job')
        self.assertEqual(data['jobs'][1]['job_id'], '00000000-0000-0000-0000-000000000000')

    def test_get_jobs_listing_sorted_by_start_date_ascendant(self):
        url = '/api/v1/projects/{}/job_listing?sort=start_time'
        resp = self.client.get(url.format('default'))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(data['jobs'][1]['job_id'], 'my job')
