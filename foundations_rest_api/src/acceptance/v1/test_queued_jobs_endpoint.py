"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
import unittest
from test.v1.models.jobs_tests_helper_mixin import JobsTestsHelperMixin
from acceptance.api_acceptance_test_case_base import APIAcceptanceTestCaseBase


class TestQueuedJobsEndpoint(JobsTestsHelperMixin, APIAcceptanceTestCaseBase):
    url = '/api/v1/projects/<project_name>/jobs/queued'
    sorting_columns = []

    def setUp(self):
        self._setup_deployment('QUEUED')
        self._setup_results_archiving()
        self._project_name = 'hana'
        self._setup_three_jobs()

    def tearDown(self):
        self._cleanup()

    def _setup_three_jobs(self):
        def method():
            from foundations.stage_logging import log_metric
            log_metric('loss', 15.33)

        self._pipeline_context.provenance.project_name = self._project_name
        self._make_queued_job('00000000-0000-0000-0000-000000000001', 123456789, 9999, 'soju hero')
        self._make_queued_job('00000000-0000-0000-0000-000000000002', 222222222, 9999, 'jade katana')

    def test_get_route(self):
        data = super(TestQueuedJobsEndpoint, self).test_get_route()
        self.assertEqual(data['queued_jobs'][0]['job_id'], '00000000-0000-0000-0000-000000000001')
        self.assertEqual(data['queued_jobs'][1]['job_id'], '00000000-0000-0000-0000-000000000002')
