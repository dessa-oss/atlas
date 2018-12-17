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


class TestJobListingNaNs(APIAcceptanceTestCaseBase):
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
        def stage0():
            return float('nan')

        @create_stage
        def stage1():
            return np.nan

        @create_stage
        def stage2(value1, value2, value3):
            foundations.log_metric('nan_metric_1', value1)
            foundations.log_metric('nan_metric_2', value2)
            foundations.log_metric('int_metric', value3)

        set_project_name(klass._project_name)
        value1 = stage0()
        value2 = stage1()
        stage2(value1, value2, 5).run()

    def test_get_route(self):
        data = super(TestJobListingNaNs, self).test_get_route()
        output_metric_data = data['jobs'][0]['output_metrics']
        result_list = [output_metric_data[0]['value'], output_metric_data[1]['value'], output_metric_data[2]['value']]
        expected_list = [None, None, 5]
        self.assertCountEqual(result_list, expected_list)
