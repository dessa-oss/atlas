"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import os

from lib.utils.filtering import filter_pyc

def all_files():
    for directory_name, _, files in os.walk('.'):
        yield from filter_pyc(directory_name, files)