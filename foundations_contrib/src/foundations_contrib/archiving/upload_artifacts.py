"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def upload_artifacts(job_id):
    from foundations_contrib.archiving.file_names_for_artifacts_path import file_names_for_artifacts_path
    from foundations_contrib.archiving import get_pipeline_archiver_for_job
    from foundations_contrib.global_state import config_manager
    from os import walk

    pipeline_archiver = get_pipeline_archiver_for_job(job_id)

    artifact_path = config_manager['artifact_path']
    artifact_path_crawl = walk(artifact_path)
    list_of_files_to_upload = list(file_names_for_artifacts_path(artifact_path_crawl))
    target_file_names = [_file_name_without_artifact_path(artifact_path, file_name) for file_name in list_of_files_to_upload]
    pipeline_archiver.append_miscellaneous('job_artifact_listing.pkl', target_file_names)

    for file_name in list_of_files_to_upload:
        pipeline_archiver.append_persisted_file(file_name, _file_name_without_artifact_path(artifact_path, file_name))
    
def _file_name_without_artifact_path(artifact_path, file_name):
    return file_name.split(artifact_path + '/')[1]