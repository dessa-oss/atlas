"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def file_names_for_artifacts_path(list_of_paths_from_os_walk):
    for directory, _, files in list_of_paths_from_os_walk:
        yield from _file_paths_for_directory(directory, files)
        

def _file_paths_for_directory(directory, files):
    from os.path import join

    for file_name in files:
        yield join(directory, file_name)