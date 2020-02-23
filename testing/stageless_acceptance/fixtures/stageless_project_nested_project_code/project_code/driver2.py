
from lib.list_dir import all_files

expected_files = set(
    [
        './config/execution/default.config.yaml',
        './config/submission/scheduler.config.yaml',
        './data/nested/more_data.csv',
        './project_code/model.py',
        './project_code/driver2.py',
        './data/other_data.csv',
        './project_code/lib/list_dir.py',
        './data/some_data.csv',
        './project_code/lib/utils/__init__.py',
        './project_code/lib/__init__.py',
        './project_code/lib/utils/filtering.py',
        './project_code/driver.py'
    ]
)

import os

actual_files = set(all_files())

if expected_files.issubset(actual_files):
    print('found all expected files in cwd!')
else:
    print('expected to find {} in {} but did not'.format(expected_files, actual_files))