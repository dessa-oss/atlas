"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Kyle De Freitas <k.defreitas@dessa.com>, 08 2019
"""

def artifact_listing_for_job(job_id, archive):
    raw_file_paths = archive.list_files('user_artifacts/*', job_id)
    
    artifacts = []
    for file_path in raw_file_paths:
        artifacts.append(file_path.split("/")[-1])
    
    return artifacts