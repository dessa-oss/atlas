"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class DataContractOptions(object):
    
    def __init__(self, max_bins=None, check_schema=None, check_row_count=None, special_values=None, check_distribution=None, distribution=None):
        self.max_bins = max_bins
        self.check_schema = check_schema
        self.check_row_count = check_row_count
        self.special_values = special_values
        self.check_distribution = check_distribution
        self.distribution = distribution

    def __eq__(self, other):
        return isinstance(other, DataContractOptions) \
            and self._special_values_equal(other) \
            and self._other_attributes_equal(other)

    def _other_attributes_equal(self, other):
        return self.max_bins == other.max_bins \
            and self.check_schema == other.check_schema \
            and self.check_row_count == other.check_row_count \
            and self.check_distribution == other.check_distribution \
            and self.distribution == other.distribution

    def _special_values_equal(self, other):
        if self.special_values is None:
            return other.special_values is None

        return len(self.special_values) == len(other.special_values) and _zipped_elements_equal(self.special_values, other.special_values)

def _equality_check(value, other_value):
    import math

    if math.isnan(value):
        return math.isnan(other_value)

    return value == other_value

def _zipped_elements_equal(values, other_values):
    for value, other_value in zip(values, other_values):
        if not _equality_check(value, other_value):
            return False

    return True