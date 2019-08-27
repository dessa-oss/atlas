"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def submit(arguments):
    from foundations_contrib.cli.job_submission.config import load
    from foundations_contrib.change_directory import ChangeDirectory
    import os

    current_directory = os.getcwd()
    with ChangeDirectory(arguments.job_dir or current_directory):
        load(arguments.scheduler_config or 'scheduler')
