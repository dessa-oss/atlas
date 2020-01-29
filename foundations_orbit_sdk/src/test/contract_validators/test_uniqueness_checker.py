"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Calvin Choi <c.choi@dessa.com>, 01 2020
"""

import numpy as np
import pandas as pd
from foundations_spec import *
from foundations_orbit.contract_validators.uniqueness_checker import UniquenessChecker
import string
from hypothesis import given, assume, example, settings
import hypothesis.strategies as st
from hypothesis.extra.pandas import column, data_frames

@st.composite
def dataframes(draw, *strategies: st.SearchStrategy) -> st.SearchStrategy:
    names = draw(st.lists(st.text(min_size=1), unique=True, min_size=1))
    cols = [column(name, elements=draw(st.sampled_from(strategies)), unique=True) for name in names]
    return draw(data_frames(cols))

class TestUniquenessChecker(Spec):

    # All of this run before each test, trying to avoid using bulky let_now syntax for initialization
    @set_up
    def set_up(self):
        self.uniqueness_checker = UniquenessChecker()
        self.column_name = self.faker.word()
        self.column_name_two = self.faker.word()

    def test_uniqueness_checker_validate_with_empty_dataframe_returns_boilerplate_result(self):
        expected = {
            'summary': {
                'healthy': 0,
                'critical': 0,
                'warning': 0
            },
            'details_by_attribute': []
        }
        self.assertEqual(expected, self.uniqueness_checker.validate(pd.DataFrame()))


    def test_uniqueness_checker_validate_with_one_column_passes(self):
        expected_result = {
            'summary': self._generate_summary_dictionary(healthy=1),
            'details_by_attribute': [{
                'attribute_name': self.column_name,
                'validation_outcome': 'healthy'
            }]
        }

        self.uniqueness_checker.configure(attributes=[self.column_name])
        self.assertEqual(expected_result, self.uniqueness_checker.validate(self._generate_unique_dataframe([self.column_name], int)))

    def test_uniqueness_checker_validate_only_runs_test_on_configured_columns(self):
        dataframe_to_validate = self._generate_unique_dataframe([self.column_name, self.column_name_two], int)

        self.uniqueness_checker.configure(attributes=[self.column_name_two])

        expected_result = {
            'summary': self._generate_summary_dictionary(healthy=1),
            'details_by_attribute': [{
                'attribute_name': self.column_name_two,
                'validation_outcome': 'healthy'
            }]
        }

        self.assertEqual(expected_result, self.uniqueness_checker.validate(dataframe_to_validate))

    @given(dataframes(st.booleans()))
    def test_uniqueness_checker_using_hypothesis_bools(self, df):
        self._hypothesis_run_validation_against_same_dataframe(df)

    @given(dataframes(st.text(alphabet=string.ascii_lowercase)))
    def test_uniqueness_checker_using_hypothesis_strings(self, df):
        self._hypothesis_run_validation_against_same_dataframe(df)

    @given(dataframes(st.integers()))
    def test_uniqueness_checker_using_hypothesis_numbers(self, df):
        self._hypothesis_run_validation_against_same_dataframe(df)

    def _hypothesis_run_validation_against_same_dataframe(self, df):
        assume(not df.empty)

        uniqueness_checker = UniquenessChecker()
        with self.assert_does_not_raise():
            uniqueness_checker.configure(attributes=list(df.columns))
            actual_result = uniqueness_checker.validate(df)

            expected_result = {
                'summary': self._generate_summary_dictionary(healthy=len(df.columns)),
                'details_by_attribute': [{
                    'attribute_name': column_name,
                    'validation_outcome': 'healthy'
                } for column_name in df.columns]
            }

            self.assertCountEqual(expected_result['details_by_attribute'], actual_result['details_by_attribute'])

    def _generate_unique_dataframe(self, column_names, dtype, min=-10, max=10):
        data = {}
        for column in column_names:
            if dtype == int:
                data[column] = list(range(min, max))

        return pd.DataFrame(data)
    
    def _generate_summary_dictionary(self, healthy=0, critical=0, warning=0):
        return {
                'healthy': healthy,
                'critical': critical,
                'warning': warning
            }