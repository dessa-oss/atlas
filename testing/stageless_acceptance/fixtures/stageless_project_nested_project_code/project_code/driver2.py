"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import os

def all_files():
    for directory_name, _, files in os.walk('.'):
        for file_name in files:
            if not file_name.endswith('.pyc'):
                yield os.path.join(directory_name, file_name)

expected_files = set(
    [
        './project_code/driver.py',
        './project_code/model.py',
        './project_code/driver2.py',
        './config/local.config.yaml',
        './data/some_data.csv',
        './data/other_data.csv',
        './data/nested/more_data.csv'
    ]
)

actual_files = set(all_files())

if expected_files.issubset(actual_files):
    print('found all expected files in cwd!')
else:
    print('expected to find {} in {} but did not'.format(expected_files, actual_files))