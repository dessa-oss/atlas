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
        import math

        if not isinstance(other, DataContractOptions):
            return False

        if len(self.special_values) != len(other.special_values):
            return False

        for value, other_value in zip(self.special_values, other.special_values):
            if not _equality_check(value, other_value):
                return False

        return True

def _equality_check(value, other_value):
    import math

    if math.isnan(value):
        return math.isnan(other_value)

    return value == other_value