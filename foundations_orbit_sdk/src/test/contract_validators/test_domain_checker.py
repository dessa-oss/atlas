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
        import pandas

        empty_dataframe = pandas.DataFrame({})
        expected_result = {}
        self.assertEqual(expected_result, self.domain_checker.validate(empty_dataframe))

    def test_domain_checker_passes_when_configured_and_reference_dataframe_used_when_validating(self):
        column_name = self.faker.word()
        self.domain_checker.configure(attributes=[column_name])

        df = self._generate_dataframe([column_name], int, 100)
        self.domain_checker.calculate_stats_from_dataframe(df)

        expected_result = {column_name: {'status': 'passed'}}
        self.assertEqual(expected_result, self.domain_checker.validate(df))
    
    def test_domain_checker_fails_when_column_configured_but_domain_out_of_range(self):
        pass

    def _generate_dataframe(self, column_names, dtype, length):
        import pandas, numpy
        data = {}

        if dtype == int:
            for column in column_names:
                data[column] = np.random.randint(-100, 100, length)

        return pandas.DataFrame(data)