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


class TestJobListingTrimCharacters(APIAcceptanceTestCaseBase):
    url = '/api/v2beta/projects/{_project_name}/job_listing'
    sorting_columns = []
    filtering_columns = []

    @classmethod
    def setUpClass(klass):
        klass._project_name = 'hanna'
        klass._run_stages()

    @classmethod
    def _run_stages(klass):

        @create_stage
        def stage0(value1):
            foundations.log_metric('int_metric', value1)

        set_project_name(klass._project_name)
        stage0('5' * 5000).run()

    def test_get_route(self):
        data = super(TestJobListingTrimCharacters, self).test_get_route()
        self.assertEqual(data['jobs'][0]['output_metrics'][0]['value'], '5' * 100)
