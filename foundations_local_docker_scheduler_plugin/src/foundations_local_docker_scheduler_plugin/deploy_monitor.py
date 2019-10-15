"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def job_bundle(bundle_name):
    from foundations_contrib.job_bundler import JobBundler
    from foundations_contrib.job_bundling.empty_job import EmptyJob
    from foundations_contrib.job_bundling.folder_job_source_bundle import FolderJobSourceBundle
    from foundations_contrib.global_state import config_manager

    return JobBundler(bundle_name, config_manager.config(), EmptyJob(), FolderJobSourceBundle(), 'job_source')