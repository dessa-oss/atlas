"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit import DataContract
from foundations_orbit_rest_api.v1.controllers.data_contract_summary_controller import DataContractSummaryController


class TestDataContractSummary(Spec):

    @let
    def reference_dataframe_with_one_numerical_column(self):
        import pandas
        import numpy

        values = []
        for i in range(1, 12):
            for _ in range(i):
                values.append(i)

        return pandas.DataFrame(data={'feat_1': values}, dtype=numpy.float64)

    @let
    def reference_dataframe_with_two_numerical_columns(self):
        import pandas
        import numpy

        values_1 = []
        for i in range(1, 12):
            for _ in range(i):
                values_1.append(i)

        values_2 = []
        for i in range(1, 12):
            for _ in range(i):
                values_2.append(12 - i)

        return pandas.DataFrame(data={'feat_1': values_1, 'feat_2': values_2}, dtype=numpy.float64)

    @let
    def dataframe_to_validate_with_one_numerical_column(self):
        import pandas
        import numpy

        values = []
        for i in range(1, 12):
            for _ in range(i):
                values.append(12 - i)

        return pandas.DataFrame(data={'feat_1': values}, dtype=numpy.float64)

    @let
    def dataframe_to_validate_with_one_numerical_column_and_nans(self):
        import pandas
        import numpy

        values = []
        for i in range(1, 12):
            for _ in range(i):
                values.append(12 - i)
        nans = [numpy.nan] * 9
        values.extend(nans)

        return pandas.DataFrame(data={'feat_1': values}, dtype=numpy.float64)

    @let
    def dataframe_to_validate_with_two_numerical_columns(self):
        import pandas
        import numpy

        values_1 = []
        for i in range(1, 12):
            for _ in range(i):
                values_1.append(12 - i)

        values_2 = []
        for i in range(1, 12):
            for _ in range(i):
                values_2.append(i)

        return pandas.DataFrame(data={'feat_1': values_1, 'feat_2': values_2}, dtype=numpy.float64)

    @let
    def contract_name(self):
        return self.faker.word()

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def monitor_name(self):
        return self.faker.word()

    @let
    def controller(self):
        return DataContractSummaryController()

    @set_up
    def set_up(self):
        import os

        import numpy
        numpy.random.seed(42)

        self._old_project_name = os.environ.get('PROJECT_NAME')
        self._old_monitor_name = os.environ.get('MONITOR_NAME')

        os.environ['PROJECT_NAME'] = self.project_name
        os.environ['MONITOR_NAME'] = self.monitor_name

        self.controller.params = {
            'project_name': self.project_name,
            'monitor_package': self.monitor_name,
            'data_contract': self.contract_name
        }

    @tear_down
    def tear_down(self):
        import os

        if self._old_project_name is not None:
            os.environ['PROJECT_NAME'] = self._old_project_name
        elif 'PROJECT_NAME' in os.environ:
            os.environ.pop('PROJECT_NAME')

        if self._old_monitor_name is not None:
            os.environ['MONITOR_NAME'] = self._old_monitor_name
        elif 'MONITOR_NAME' in os.environ:
            os.environ.pop('MONITOR_NAME')

    def test_validating_dataframe_creates_summary_which_is_retrieved_from_rest_api(self):
        import datetime

        summary_for_feat_1 = {
            'expected_data_summary': {
                'percentage_missing': 0.0,
                'minimum': 1,
                'maximum': 11
            },
            'actual_data_summary': {
                'percentage_missing': 0.0,
                'minimum': 1,
                'maximum': 11
            },
            'binned_data': {
                'bins': ['1.0-2.0', '2.0-3.0', '3.0-4.0', '4.0-5.0', '5.0-6.0', '6.0-7.0', '7.0-8.0', '8.0-9.0',
                         '9.0-10.0', '10.0-11.0'],
                'data': {
                    'expected_data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 21],
                    'actual_data': [11, 10, 9, 8, 7, 6, 5, 4, 3, 3]
                }
            }
        }

        inference_date = datetime.datetime.today()

        data_contract = DataContract(self.contract_name, df=self.reference_dataframe_with_one_numerical_column)
        data_contract.validate(self.dataframe_to_validate_with_one_numerical_column, inference_date)

        self.controller.params['inference_period'] = inference_date
        self.controller.params['attribute'] = 'feat_1'
        self.assertEqual(summary_for_feat_1, self.controller.index().as_json())

    def test_validating_dataframe_with_nans_creates_summary_which_is_retrieved_from_rest_api(self):
        import datetime

        summary_for_feat_1 = {
            'expected_data_summary': {
                'percentage_missing': 0.0,
                'minimum': 1,
                'maximum': 11
            },
            'actual_data_summary': {
                'percentage_missing': 0.12,
                'minimum': 1,
                'maximum': 11
            },
            'binned_data': {
                'bins': ['1.0-2.0', '2.0-3.0', '3.0-4.0', '4.0-5.0', '5.0-6.0', '6.0-7.0', '7.0-8.0', '8.0-9.0',
                         '9.0-10.0', '10.0-11.0'],
                'data': {
                    'expected_data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 21],
                    'actual_data': [11, 10, 9, 8, 7, 6, 5, 4, 3, 3]
                }
            }
        }

        inference_date = datetime.datetime.today()

        data_contract = DataContract(self.contract_name, df=self.reference_dataframe_with_one_numerical_column)
        data_contract.validate(self.dataframe_to_validate_with_one_numerical_column_and_nans, inference_date)

        self.controller.params['inference_period'] = inference_date
        self.controller.params['attribute'] = 'feat_1'
        self.assertEqual(summary_for_feat_1, self.controller.index().as_json())

    def test_validating_dataframe_with_two_columns_creates_summary_which_is_retrieved_from_rest_api(self):
        import datetime

        summary_for_feat_1 = {
            'expected_data_summary': {
                'percentage_missing': 0.0,
                'minimum': 1.0,
                'maximum': 11.0
            },
            'actual_data_summary': {
                'percentage_missing': 0.0,
                'minimum': 1.0,
                'maximum': 11.0
            },
            'binned_data': {
                'bins': ['1.0-2.0', '2.0-3.0', '3.0-4.0', '4.0-5.0', '5.0-6.0', '6.0-7.0', '7.0-8.0', '8.0-9.0',
                         '9.0-10.0', '10.0-11.0'],
                'data': {
                    'expected_data': [11, 10, 9, 8, 7, 6, 5, 4, 3, 3],
                    'actual_data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 21]
                }
            }
        }

        inference_date = datetime.datetime.today()

        data_contract = DataContract(self.contract_name, df=self.reference_dataframe_with_two_numerical_columns)
        data_contract.validate(self.dataframe_to_validate_with_two_numerical_columns, inference_date)

        self.maxDiff = None
        self.controller.params['inference_period'] = inference_date
        self.controller.params['attribute'] = 'feat_2'
        self.assertEqual(summary_for_feat_1, self.controller.index().as_json())
