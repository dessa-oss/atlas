"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.models.property_model import PropertyModel

class DataContractOptions(PropertyModel):
    
    max_bins = PropertyModel.define_property()
    check_schema = PropertyModel.define_property()
    check_row_count = PropertyModel.define_property()
    special_values = PropertyModel.define_property()
    check_distribution = PropertyModel.define_property()
    distribution = PropertyModel.define_property()

    def __eq__(self, other):
        return isinstance(other, DataContractOptions) \
            and len(self.special_values) == len(other.special_values) \
            and _zipped_elements_equal(self.special_values, other.special_values)

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