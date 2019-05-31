"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def upload_artifacts(job_id):
    from foundations_contrib.archiving.artifact_path_crawl import artifact_path_crawl
    from foundations_contrib.archiving.file_names_for_artifacts_path import file_names_for_artifacts_path
    from foundations_contrib.archiving import get_pipeline_archiver_for_job

    pipeline_archiver = get_pipeline_archiver_for_job(job_id)

    list_of_files_to_upload = list(file_names_for_artifacts_path(artifact_path_crawl()))
    pipeline_archiver.append_miscellaneous('job_artifact_listing.pkl', list_of_files_to_upload)

    for file_name in list_of_files_to_upload:
        pipeline_archiver.append_persisted_file(file_name, file_name)
    