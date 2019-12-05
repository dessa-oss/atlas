"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class Checker(object):
    
    @staticmethod
    def find_invalid_attributes(allowed_column_types, reference_column_types):
        invalid_attributes = []
        if reference_column_types == dict():
            return invalid_attributes

        for col_name, col_type in reference_column_types.items():
            if not any([allowed_type in col_type for allowed_type in allowed_column_types]):
                invalid_attributes.append(col_name)

        return invalid_attributes
