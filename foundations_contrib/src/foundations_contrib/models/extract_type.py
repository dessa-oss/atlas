"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.utils import is_string, is_number
import numbers

def extract_type(value):
    if isinstance(value, bool):
        return 'bool'

    if is_number(value):
        return 'number'

    if is_string(value):
        return 'string'

    if isinstance(value, list):
        return 'array ' + extract_type(value[0])

    return 'unknown'
