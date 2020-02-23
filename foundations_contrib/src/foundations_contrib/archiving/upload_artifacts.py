
def upload_artifacts(job_id):
    from foundations_contrib.archiving import get_pipeline_archiver_for_job

    if _artifact_path() is not None:
        pipeline_archiver = get_pipeline_archiver_for_job(job_id)
        _upload_artifacts_to_archiver(pipeline_archiver)

def _upload_artifacts_to_archiver(pipeline_archiver):
    list_of_files_to_upload = list_of_files_to_upload_from_artifact_path(_artifact_path())

    _upload_file_listing(list_of_files_to_upload, pipeline_archiver)
    _upload_artifact_files_to_archiver(list_of_files_to_upload, pipeline_archiver)

def _upload_artifact_files_to_archiver(list_of_files_to_upload, pipeline_archiver):
    for file_name in list_of_files_to_upload:
        pipeline_archiver.append_persisted_file(_file_name_without_artifact_path(file_name), file_name)

def list_of_files_to_upload_from_artifact_path(artifact_path):
    from foundations_contrib.archiving.file_names_for_artifacts_path import file_names_for_artifacts_path
    from os import walk

    artifact_path_crawl = walk(artifact_path)
    return list(file_names_for_artifacts_path(artifact_path_crawl))

def _upload_file_listing(list_of_files_to_upload, pipeline_archiver):
    target_file_names = [_file_name_without_artifact_path(file_name) for file_name in list_of_files_to_upload]
    pipeline_archiver.append_miscellaneous('job_artifact_listing.pkl', target_file_names)
    
def _file_name_without_artifact_path(file_name):
    import os
    return file_name.split(_artifact_path() + os.path.sep)[1]

def _artifact_path():
    from foundations_contrib.global_state import config_manager
    return config_manager.config().get('artifact_path')
