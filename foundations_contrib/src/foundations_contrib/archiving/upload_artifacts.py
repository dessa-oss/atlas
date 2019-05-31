"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def upload_artifacts():
    from foundations_contrib.archiving.artifact_path_crawl import artifact_path_crawl
    from foundations_contrib.archiving.file_names_for_artifacts_path import file_names_for_artifacts_path

    file_names_for_artifacts_path(artifact_path_crawl())
