"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit.contract_validators.row_count_checker import RowCountChecker

class TestRowCountChecker(Spec):

    def test_row_count_difference_is_zero_if_both_row_counts_are_equal(self):
        checker = RowCountChecker(1)
        self.assertEqual(0.0, checker.validate(1))

    def test_row_count_difference_is_100_percent_if_current_row_count_is_twice_the_reference(self):
        checker = RowCountChecker(1)
        self.assertEqual(1.0, checker.validate(2))

    def test_row_count_difference_is_300_percent_if_current_row_count_is_four_times_the_reference(self):
        checker = RowCountChecker(1)
        self.assertEqual(3.0, checker.validate(4))

    def test_row_count_difference_is_50_percent_if_current_row_count_is_half_the_reference(self):
        checker = RowCountChecker(2)
        self.assertEqual(0.5, checker.validate(1))
