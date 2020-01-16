"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 12 2018
"""
import numpy as np
import foundations
from foundations import set_project_name
from acceptance.api_acceptance_test_case_base import APIAcceptanceTestCaseBase
from acceptance.v2beta.jobs_tests_helper_mixin_v2 import JobsTestsHelperMixinV2
from foundations_spec import *

@skip
class TestJobListingTrimCharacters(JobsTestsHelperMixinV2, APIAcceptanceTestCaseBase):
    url = '/api/v2beta/projects/{_project_name}/job_listing'
    sorting_columns = []
    filtering_columns = []

    @classmethod
    def setUpClass(klass):
        JobsTestsHelperMixinV2.setUpClass()
        klass._set_project_name('hanna')
        klass._run_stages()

    @set_up
    def set_up(self):
        import os
        from foundations_contrib.global_state import redis_connection

        os.environ['FOUNDATIONS_HOME'] = os.getenv('FOUNDATIONS_HOME', '')
        redis_connection.flushall()
        self.submit_job()

    def submit_job(self):
        import subprocess

        submit_result = subprocess.run('foundations submit scheduler acceptance/v2beta/fixtures log_int_metric.py')
        self.assertEqual(0, submit_result.returncode)

    @classmethod
    def _run_stages(klass):

        def stage0(value1):
            from foundations.stage_logging import log_metric
            log_metric('int_metric', value1)

        job_name = 'test job'
        klass._pipeline_context.file_name = job_name
        stage = klass._pipeline.stage(stage0, '5' * 5000)
        stage.run_same_process()
        klass._make_completed_job(job_name, 'default user')

    def test_get_route(self):
        data = super(TestJobListingTrimCharacters, self).test_get_route()
        self.assertEqual(data['jobs'][0]['output_metrics'][0]['value'], '5' * 100)
