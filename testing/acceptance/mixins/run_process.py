"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def run_process(command, directory):
    import subprocess
    from foundations_contrib.change_directory import ChangeDirectory

    with ChangeDirectory(directory):
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
    out, err = process.communicate()

    return out.decode()
