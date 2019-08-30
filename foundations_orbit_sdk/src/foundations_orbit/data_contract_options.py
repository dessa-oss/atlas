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