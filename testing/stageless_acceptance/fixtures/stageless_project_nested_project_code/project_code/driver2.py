"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from lib.list_dir import all_files

expected_files = set(
    [
        './config/local.config.yaml',
        './data/nested/more_data.csv',
        './project_code/model.py',
        './project_code/driver2.py',
        './data/other_data.csv',
        './lib/list_dir.py',
        './data/some_data.csv',
        './lib/utils/__init__.py',
        './lib/__init__.py',
        './lib/utils/filtering.py',
        './project_code/driver.py'
    ]
)

actual_files = set(all_files())

if expected_files.issubset(actual_files):
    print('found all expected files in cwd!')
else:
    print('expected to find {} in {} but did not'.format(expected_files, actual_files))