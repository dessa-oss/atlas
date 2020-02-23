
from foundations_spec import *
from foundations_orbit.contract_validators.domain_checker import DomainChecker, ALL_CATEGORIES

import numpy as np
import pandas as pd
import string

from hypothesis import given, assume, example, settings, HealthCheck
import hypothesis.strategies as st
from hypothesis.extra.pandas import column, data_frames

@st.composite
def dataframes(draw, *strategies: st.SearchStrategy) -> st.SearchStrategy:
    names = draw(st.lists(st.text(min_size=1), unique=True, min_size=1))
    cols = [column(name, elements=draw(st.sampled_from(strategies))) for name in names]
    return draw(data_frames(cols))

class TestDomainChecker(Spec):

    # All of this run before each test, trying to avoid using bulky let_now syntax for initialization
    @set_up
    def set_up(self):
        self.domain_checker = DomainChecker()
        self.column_name = self.faker.word()
        self.column_name_two = self.faker.word()

    def test_domain_checker_works_with_int_data_type_when_validating_against_itself(self):
        self._test_healthy_result_when_validating_dataframe_against_itself(dtype=int)

    def test_domain_checker_works_with_boolean_data_type_when_validating_against_itself(self):
        self._test_healthy_result_when_validating_dataframe_against_itself(dtype=bool)

    def test_domain_checker_works_with_string_data_type_when_validating_against_itself(self):
        self._test_healthy_result_when_validating_dataframe_against_itself(dtype=str)

    def test_domain_checker_works_with_datetime_data_type_when_validating_against_itself(self):
        self._test_healthy_result_when_validating_dataframe_against_itself(dtype='datetime')
    
    def test_domain_checker_works_with_category_data_type_when_validating_against_itself(self):
        self._test_healthy_result_when_validating_dataframe_against_itself(dtype='category')

    def test_validate_with_no_columns_configured_returns_empty_results(self):
        empty_dataframe = pd.DataFrame({})
        expected_result = {
            'summary': self._generate_summary_dictionary(),
            'details_by_attribute': []
        }
        self.assertEqual(expected_result, self.domain_checker.validate(empty_dataframe))

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

    def test_domain_checker_uses_manually_configured_domain(self):
        self.maxDiff = None
        df = self._generate_dataframe([self.column_name], int)

        config = {
            self.column_name: [1,2,3,4] # Pick random values for domain
        }

        self.domain_checker.configure(configuration=config)
        self.domain_checker.calculate_stats_from_dataframe(df)

        expected_result = {
            'summary': self._generate_summary_dictionary(critical=1),
            'details_by_attribute': [{
                'attribute_name': self.column_name,
                'validation_outcome': 'critical',
                'values_out_of_bounds': [v for v in list(df[self.column_name]) if v not in config[self.column_name]],
                'percentage_out_of_bounds': (df[self.column_name].size - len(config[self.column_name])) / df[self.column_name].size
            }]
        }
        self.assertEqual(expected_result, self.domain_checker.validate(df))

    def test_domain_checker_uses_manually_configured_domain_with_all_categories_constant(self):
        self.maxDiff = None
        df = self._generate_dataframe([self.column_name], int)

        config = {
            self.column_name: ALL_CATEGORIES
        }

        self.domain_checker.configure(configuration=config)
        self.domain_checker.calculate_stats_from_dataframe(df)

        expected_result = {
            'summary': self._generate_summary_dictionary(healthy=1),
            'details_by_attribute': [{
                'attribute_name': self.column_name,
                'validation_outcome': 'healthy'
            }]
        }
        self.assertEqual(expected_result, self.domain_checker.validate(df))

    def _test_healthy_result_when_validating_dataframe_against_itself(self, dtype):
        self.domain_checker.configure(attributes=self.column_name)
        df = self._generate_dataframe([self.column_name], dtype)
        self.domain_checker.calculate_stats_from_dataframe(df)

        expected_result = {
            'summary': self._generate_summary_dictionary(healthy=1),
            'details_by_attribute': [{
                'attribute_name': self.column_name,
                'validation_outcome': 'healthy'
            }]
        }
        self.assertEqual(expected_result, self.domain_checker.validate(df))

    def test_value_error_when_configuring_with_no_parameters(self):
        with self.assertRaises(ValueError):
            self.domain_checker.configure()

    def test_value_error_when_configuring_with_both_parameters(self):
        with self.assertRaises(ValueError):
            self.domain_checker.configure(['some_string'], {'some_string_2': ['some_string_3']})

    def test_value_error_when_configuring_with_none_string_or_list_attributes(self):
        with self.assertRaises(ValueError):
            self.domain_checker.configure(3)

    def test_value_error_when_configuring_with_none_string_or_list_configuration(self):
        with self.assertRaises(ValueError):
            self.domain_checker.configure(configuration=3)

    def test_value_error_when_configuring_with_configuration_of_non_string_key(self):
        with self.assertRaises(ValueError):
            self.domain_checker.configure(configuration={
                3: ['some_string']
            })

    def test_value_error_when_configuring_with_configuration_of_non_list_key(self):
        with self.assertRaises(ValueError):
            self.domain_checker.configure(configuration={
                'some_string': 3
            })

    def test_info_method_returns_info_about_domain_checker(self):
        df = self._generate_dataframe([self.column_name], int)
        self.domain_checker.calculate_stats_from_dataframe(df)
        self.domain_checker.configure(attributes=self.column_name)

        expected_result = {
            'reference_dataframe_unique': {col: list(df[col]) for col in df.columns},
            'configured_attributes': {
                self.column_name: ALL_CATEGORIES
            }
        }

        actual_result = self.domain_checker.info()

        self.assertEqual(expected_result, actual_result)

    def test_str_method_returns_info_about_domain_checker(self):
        df = self._generate_dataframe([self.column_name], int)
        self.domain_checker.calculate_stats_from_dataframe(df)
        self.domain_checker.configure(attributes=self.column_name)

        expected_result = str({
            'reference_dataframe_unique': {col: list(df[col]) for col in df.columns},
            'configured_attributes': {
                self.column_name: ALL_CATEGORIES
            }
        })

        self.assertEqual(expected_result, str(self.domain_checker))


    @given(dataframes(st.booleans()))
    @settings(suppress_health_check=[HealthCheck.too_slow])
    def test_domain_checker_using_hypothesis_bools(self, df):
        self._hypothesis_run_validation_against_same_dataframe(df)

    @given(dataframes(st.text(alphabet=string.ascii_lowercase)))
    def test_domain_checker_using_hypothesis_strings(self, df):
        self._hypothesis_run_validation_against_same_dataframe(df)

    @given(dataframes(st.integers()))
    def test_domain_checker_using_hypothesis_numbers(self, df):
        self._hypothesis_run_validation_against_same_dataframe(df)

    def _hypothesis_run_validation_against_same_dataframe(self, df):
        assume(not df.empty)

        domain_checker = DomainChecker()
        with self.assert_does_not_raise():
            domain_checker.calculate_stats_from_dataframe(df)
            domain_checker.configure(attributes=list(df.columns))
            actual_result = domain_checker.validate(df)

            expected_result = {
                'summary': self._generate_summary_dictionary(healthy=len(df.columns)),
                'details_by_attribute': [{
                    'attribute_name': column_name,
                    'validation_outcome': 'healthy'
                } for column_name in df.columns]
            }

            self.assertEqual(expected_result, actual_result)

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
                data[column] = [self.faker.date() for _ in range(100)]
            elif dtype == 'category':
                return self._generate_dataframe([self.column_name], dtype=str).astype('category')

        return pd.DataFrame(data)

    def _generate_summary_dictionary(self, healthy=0, critical=0, warning=0):
        return {
                'healthy': healthy,
                'critical': critical,
                'warning': warning
            }