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
    def test_validate_with_no_columns_configured_returns_empty_results(self):
        import pandas

        empty_dataframe = pandas.DataFrame({})
        expected_result = {}
        self.assertEqual(expected_result, DomainChecker().validate(empty_dataframe))

    def test_domain_checker_passes_when_configured_and_reference_dataframe_used_when_validating(self):
        domain_checker = DomainChecker()
        column_name = self.faker.word()
        domain_checker.configure(attributes=[column_name])

        df = self._generate_dataframe([column_name], int, 100)

        domain_checker.calculate_stats_from_dataframe(df)

        expected_result = {column_name: {'status': 'passed'}}

        self.assertEqual(expected_result, domain_checker.validate(df))

    def _generate_dataframe(self, column_names, dtype, length):
        import pandas, numpy
        data = {}
        # numpy.random.seed = 6379

        if dtype == int:
            for column in column_names:
                data[column] = np.random.randint(-100, 100, length)

        return pandas.DataFrame(data)