"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Kyle De Freitas <k.defreitas@dessa.com>, 08 2019
"""

def artifact_listing_for_job_in_archive(job_id, archive):
    raw_file_paths = archive.list_files('user_artifacts/*', job_id)
    return list(_artifact_listing_for_paths(raw_file_paths, job_id))

def _artifact_listing_for_paths(raw_file_paths, job_id):
    for file_path in raw_file_paths:
        yield _file_path_without_artifact_prefix(file_path, job_id)

def _file_path_without_artifact_prefix(file_path, job_id):
    return file_path[_file_prefix_length(job_id):]

def _file_prefix_length(job_id):
    return len(job_id) + len('/user_artifacts/')