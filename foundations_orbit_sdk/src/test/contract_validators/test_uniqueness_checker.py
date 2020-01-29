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

class TestUniquenessChecker(Spec):

    # All of this run before each test, trying to avoid using bulky let_now syntax for initialization
    @set_up
    def set_up(self):
        self.uniqueness_checker = UniquenessChecker()
        self.column_name = self.faker.word()
        self.column_name_two = self.faker.word()

    def test_uniqueness_checker_validate_with_empty_dataframe_returns_boilerplate_result(self):
        expected = {
            'summary': {},
            'details_by_attribute': []
        }
        self.assertEqual(expected, self.uniqueness_checker.validate(pd.DataFrame()))


