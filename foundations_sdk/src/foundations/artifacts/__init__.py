"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def create_syncable_directory(key, directory_path, source_job_id=None):
    from foundations.artifacts.syncable_directory import SyncableDirectory
    from foundations_contrib.global_state import current_foundations_context
    
    job_id = current_foundations_context().pipeline_context().file_name
    return SyncableDirectory(key, directory_path, job_id, source_job_id or job_id)