"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.utils import is_string
import numbers

def extract_type(value):
    type_map = {
        bool: 'bool',
        float: 'number',
        int: 'number',
    }

    result = type_map.get(value.__class__, None)
    if result is None:
        if is_string(value):
            return 'string'
        elif isinstance(value, list):
            return 'array ' + extract_type(value[0])
        else:
            return 'unknown'
    else:
        return result
