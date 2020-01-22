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

    def test_validate_with_no_columns_configured_returns_empty_results(self):
        empty_dataframe = pd.DataFrame({})
        expected_result = {
            'summary': {
                'healthy': 0,
                'critical': 0,
                'warning': 0
            },
            'details_by_attribute': []
        }
        self.assertEqual(expected_result, self.domain_checker.validate(empty_dataframe))

    def test_domain_checker_passes_when_configured_and_reference_dataframe_used_when_validating(self):
        column_name = self.faker.word()
        self.domain_checker.configure(attributes=[column_name])

        df = self._generate_dataframe([column_name], int)
        self.domain_checker.calculate_stats_from_dataframe(df)

        expected_result = {
            'summary': {
                'healthy': 1,
                'critical': 0,
                'warning': 0
            },
            'details_by_attribute': [{
                'attribute_name': column_name,
                'validation_outcome': 'healthy'
            }]
        }
        self.assertEqual(expected_result, self.domain_checker.validate(df))

    def test_domain_checker_fails_when_column_configured_but_domain_out_of_range(self):
        column_name = self.faker.word()
        self.domain_checker.configure(attributes=[column_name])

        ref_df = self._generate_dataframe([column_name], int, min=1, max=5)
        cur_df = self._generate_dataframe([column_name], int, min=6, max=10)
        self.domain_checker.calculate_stats_from_dataframe(ref_df)

        expected_result = {
            'summary': {
                'healthy': 0,
                'critical': 1,
                'warning': 0
            },
            'details_by_attribute': [{
                'attribute_name': column_name,
                'validation_outcome': 'critical',
                'values_out_of_bounds': list(cur_df[column_name]),
                'percentage_out_of_bounds': 1
            }]
        }
        self.assertEqual(expected_result, self.domain_checker.validate(cur_df))

    def _generate_dataframe(self, column_names, dtype, min=-10, max=10):
        data = {}

        if dtype == int:
            for column in column_names:
                data[column] = list(range(min, max))

        return pd.DataFrame(data)
