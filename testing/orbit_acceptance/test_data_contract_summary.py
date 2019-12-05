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
    def column_name(self):
        return 'feat_1'

    @let
    def second_column_name(self):
        return 'feat_2'

    @let
    def reference_dataframe_with_one_numerical_column(self):
        import pandas
        import numpy

        values = []
        for i in range(1, 12):
            for _ in range(i):
                values.append(i)

        return pandas.DataFrame(data={self.column_name: values}, dtype=numpy.float64)

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

        return pandas.DataFrame(data={self.column_name: values_1, self.second_column_name: values_2}, dtype=numpy.float64)

    @let
    def dataframe_to_validate_with_one_numerical_column(self):
        import pandas
        import numpy

        values = []
        for i in range(1, 12):
            for _ in range(i):
                values.append(12 - i)

        return pandas.DataFrame(data={self.column_name: values}, dtype=numpy.float64)

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

        return pandas.DataFrame(data={self.column_name: values}, dtype=numpy.float64)

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

        return pandas.DataFrame(data={self.column_name: values_1, self.second_column_name: values_2}, dtype=numpy.float64)

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

    @let
    def inference_date(self):
        import datetime
        return datetime.datetime.today()

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

        dc = DataContract(self.contract_name, df=self.reference_dataframe_with_one_numerical_column)
        self._validate_and_assert_equal_on_column_from_api(dc, self.dataframe_to_validate_with_one_numerical_column, self.column_name, summary_for_feat_1)

    def test_validating_dataframe_with_nans_creates_summary_which_is_retrieved_from_rest_api(self):
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

        dc = DataContract(self.contract_name, df=self.reference_dataframe_with_one_numerical_column)
        self._validate_and_assert_equal_on_column_from_api(dc, self.dataframe_to_validate_with_one_numerical_column_and_nans, self.column_name, summary_for_feat_1)

    def test_validating_dataframe_with_two_columns_creates_summary_which_is_retrieved_from_rest_api(self):
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

        dc = DataContract(self.contract_name, df=self.reference_dataframe_with_two_numerical_columns)
        self._validate_and_assert_equal_on_column_from_api(dc, self.dataframe_to_validate_with_two_numerical_columns, self.second_column_name, summary_for_feat_1)

    def test_data_report_for_data_frame_with_only_one_values_against_itself(self):
        import pandas as pd
        size = 20
        summary_for_feat_2 = {
            'actual_data_summary': {
                'maximum': 2.0,
                'minimum': 2.0,
                'percentage_missing': 0.0
            },
            'binned_data': {
                'bins': [2],
                'data': {
                    'actual_data': [size], 'expected_data': [size]
                }
            },
            'expected_data_summary': {
                'maximum': 2.0,
                'minimum': 2.0,
                'percentage_missing': 0.0
            }
        }

        df = pd.DataFrame(data={
            self.column_name: [2] * size,
            self.second_column_name: [2] * size
        })
        dc = DataContract(self.contract_name, df=df)
        self._validate_and_assert_equal_on_column_from_api(dc, df, self.second_column_name, summary_for_feat_2)

    def _validate_and_assert_equal_on_column_from_api(self, data_contract, validation_dataframe, column_name, expected_results):
        data_contract.validate(validation_dataframe, self.inference_date)

        self.controller.params['inference_period'] = self.inference_date
        self.controller.params['attribute'] = column_name
        self.assertEqual(expected_results, self.controller.index().as_json())
