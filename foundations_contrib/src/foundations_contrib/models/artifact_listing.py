"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Kyle De Freitas <k.defreitas@dessa.com>, 07 2019
"""

def artifact_listing_for_job_in_archive(job_id, archive):
    raw_file_paths = archive.list_files('user_artifacts/*', job_id)
    archive_keys = _artifact_listing_for_paths(raw_file_paths, job_id)
    
    listing = [_artifact_key_with_metadata(archive, key, job_id) for key in archive_keys]
    listing.sort(key=lambda entry: entry[0])
    
    return listing

def artifact_listing_for_job(job_id):
    from foundations_contrib.archiving import load_archive
    return artifact_listing_for_job_in_archive(job_id, load_archive('artifact_archive'))

def _artifact_listing_for_paths(raw_file_paths, job_id):
    artifact_paths = _listing_without_metadata_files(raw_file_paths)
    for file_path in artifact_paths:
        yield _file_path_without_artifact_prefix(file_path, job_id)

def _listing_without_metadata_files(raw_file_paths):
    return filter(lambda filepath: not filepath.endswith('.metadata'), raw_file_paths)

def _file_path_without_artifact_prefix(file_path, job_id):
    return file_path[_file_prefix_length(job_id):]

def _file_prefix_length(job_id):
    return len(job_id) + len('/user_artifacts/')

def _artifact_key_with_metadata(artifact_archive, archive_key, job_id):
    return (archive_key, artifact_archive.fetch(f'user_artifacts/{archive_key}.metadata', job_id))