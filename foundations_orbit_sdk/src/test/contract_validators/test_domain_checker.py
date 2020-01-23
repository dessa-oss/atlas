"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_orbit.contract_validators.domain_checker import DomainChecker

import numpy as np
import pandas as pd

class TestDomainChecker(Spec):

    @set_up
    def set_up(self):
        self.domain_checker = DomainChecker()
        self.column_name = self.faker.word()
        self.column_name_two = self.faker.word()

    def test_validate_with_no_columns_configured_returns_empty_results(self):
        empty_dataframe = pd.DataFrame({})
        expected_result = {
            'summary': self._generate_summary_dictionary(),
            'details_by_attribute': []
        }
        self.assertEqual(expected_result, self.domain_checker.validate(empty_dataframe))

    def test_domain_checker_passes_when_configured_and_reference_dataframe_used_when_validating(self):
        self.domain_checker.configure(attributes=self.column_name)

        df = self._generate_dataframe([self.column_name], int)
        self.domain_checker.calculate_stats_from_dataframe(df)

        expected_result = {
            'summary': self._generate_summary_dictionary(healthy=1),
            'details_by_attribute': [{
                'attribute_name': self.column_name,
                'validation_outcome': 'healthy'
            }]
        }
        self.assertEqual(expected_result, self.domain_checker.validate(df))

    def test_domain_checker_passes_when_configured_and_reference_dataframe_with_nans_used_when_validating(self):
        self.domain_checker.configure(attributes=self.column_name)

        df = self._generate_dataframe([self.column_name], 'int_with_nan')
        self.domain_checker.calculate_stats_from_dataframe(df)

        expected_result = {
            'summary': self._generate_summary_dictionary(healthy=1),
            'details_by_attribute': [{
                'attribute_name': self.column_name,
                'validation_outcome': 'healthy'
            }]
        }
        self.assertEqual(expected_result, self.domain_checker.validate(df))

    def test_domain_checker_fails_when_column_configured_but_domain_out_of_range(self):
        self.domain_checker.configure(attributes=self.column_name)

        ref_df = self._generate_dataframe([self.column_name], int, min=1, max=5)
        cur_df = self._generate_dataframe([self.column_name], int, min=6, max=10)
        self.domain_checker.calculate_stats_from_dataframe(ref_df)

        expected_result = {
            'summary': self._generate_summary_dictionary(critical=1),
            'details_by_attribute': [{
                'attribute_name': self.column_name,
                'validation_outcome': 'critical',
                'values_out_of_bounds': list(cur_df[self.column_name]),
                'percentage_out_of_bounds': 1
            }]
        }
        self.assertEqual(expected_result, self.domain_checker.validate(cur_df))

    def test_domain_checker_fails_when_column_configured_but_domain_out_of_range_with_reference_dataframe_with_nans(self):
        self.domain_checker.configure(attributes=self.column_name)

        ref_df = self._generate_dataframe([self.column_name], 'int_with_nan', min=1, max=5)
        cur_df = self._generate_dataframe([self.column_name], int, min=6, max=10)
        self.domain_checker.calculate_stats_from_dataframe(ref_df)

        expected_result = {
            'summary': self._generate_summary_dictionary(critical=1),
            'details_by_attribute': [{
                'attribute_name': self.column_name,
                'validation_outcome': 'critical',
                'values_out_of_bounds': list(cur_df[self.column_name]),
                'percentage_out_of_bounds': 1
            }]
        }
        self.assertEqual(expected_result, self.domain_checker.validate(cur_df))

    def test_domain_checker_fails_when_column_configured_but_domain_out_of_range_with_current_dataframe_with_nans(self):
        self.domain_checker.configure(attributes=self.column_name)

        ref_df = self._generate_dataframe([self.column_name], int, min=1, max=5)
        cur_df = self._generate_dataframe([self.column_name], 'int_with_nan', min=6, max=10)
        self.domain_checker.calculate_stats_from_dataframe(ref_df)

        expected_result = {
            'summary': self._generate_summary_dictionary(critical=1),
            'details_by_attribute': [{
                'attribute_name': self.column_name,
                'validation_outcome': 'critical',
                'values_out_of_bounds': [v for v in list(cur_df[self.column_name]) if not np.isnan(v)],
                'percentage_out_of_bounds': 1.0
            }]
        }

        validation_result = self.domain_checker.validate(cur_df)

        values_out_of_bounds = validation_result['details_by_attribute'][0]['values_out_of_bounds']
        self.assertIn(True, np.isnan(values_out_of_bounds))
        validation_result['details_by_attribute'][0]['values_out_of_bounds'] = [v for v in values_out_of_bounds if not np.isnan(v)]
        self.assertEqual(expected_result, validation_result)

    def test_domain_checker_passes_on_configured_column_only_when_validated_against_itself(self):
        self.domain_checker.configure(attributes=self.column_name)

        df = self._generate_dataframe([self.column_name, self.column_name_two], int)
        self.domain_checker.calculate_stats_from_dataframe(df)

        expected_result = {
            'summary': self._generate_summary_dictionary(healthy=1),
            'details_by_attribute': [{
                'attribute_name': self.column_name,
                'validation_outcome': 'healthy'
            }]
        }
        self.assertEqual(expected_result, self.domain_checker.validate(df))

    def test_domain_checker_exclude_removes_previously_configured_column_from_validation(self):
        self.domain_checker.configure(attributes=[self.column_name, self.column_name_two])
        self.domain_checker.exclude(attributes=self.column_name)

        df = self._generate_dataframe([self.column_name, self.column_name_two], int)
        self.domain_checker.calculate_stats_from_dataframe(df)

        expected_result = {
            'summary': self._generate_summary_dictionary(healthy=1),
            'details_by_attribute': [{
                'attribute_name': self.column_name_two,
                'validation_outcome': 'healthy'
            }]
        }
        self.assertEqual(expected_result, self.domain_checker.validate(df))

    def test_domain_checker_works_with_boolean_data_type_when_validating_against_itself(self):
        self._test_healthy_result_when_validating_dataframe_against_itself(dtype=bool)

    def test_domain_checker_works_with_string_data_type_when_validating_against_itself(self):
        self._test_healthy_result_when_validating_dataframe_against_itself(dtype=str)

    def test_domain_checker_works_with_datetime_data_type_when_validating_against_itself(self):
        self._test_healthy_result_when_validating_dataframe_against_itself(dtype='datetime')

    def _test_healthy_result_when_validating_dataframe_against_itself(self, dtype):
        self.domain_checker.configure(attributes=self.column_name)
        df = self._generate_dataframe([self.column_name], bool)
        self.domain_checker.calculate_stats_from_dataframe(df)

        expected_result = {
            'summary': self._generate_summary_dictionary(healthy=1),
            'details_by_attribute': [{
                'attribute_name': self.column_name,
                'validation_outcome': 'healthy'
            }]
        }
        self.assertEqual(expected_result, self.domain_checker.validate(df))

    def _generate_dataframe(self, column_names, dtype, min=-10, max=10):
        data = {}

        for column in column_names:
            if dtype == 'int_with_nan':
                data[column] = list(range(min, max)) + [np.nan]
            elif dtype == int:
                data[column] = list(range(min, max))
            elif dtype == bool:
                data[column] = [True]*50 + [False]*50
            elif dtype == str:
                data[column] = [self.faker.word() for _ in range(100)]
            elif dtype == 'datetime':
                data[column] = [self.faker.datetime() for _ in range(100)]

        return pd.DataFrame(data)

    def _generate_summary_dictionary(self, healthy=0, critical=0, warning=0):
        return {
                'healthy': healthy,
                'critical': critical,
                'warning': warning
            }