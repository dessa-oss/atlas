"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def extract_type(value):
    from foundations.utils import is_string

    if isinstance(value, float) or isinstance(value, int):
        return 'number'
    elif is_string(value):
        return 'string'
    elif is_string(value):
        return 'bool'
    elif isinstance(value, list):
        return 'array ' + extract_type(value[0])
    else:
        return 'unknown'
