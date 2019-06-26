"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import os

def filter_pyc(directory_name, iterable):
    for file_name in iterable:
        if not file_name.endswith('.pyc'):
            yield os.path.join(directory_name, file_name)