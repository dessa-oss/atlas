

def load_archive(name):
    from foundations_contrib.global_state import config_manager
    from foundations_contrib.null_archive import NullArchive

    return config_manager.reflect_instance(name, 'archive', lambda: NullArchive())

def get_pipeline_archiver_for_job(job_id):
    from foundations_internal.pipeline_archiver import PipelineArchiver

    artifact_archive = load_archive('artifact_archive')
    job_source_archive = load_archive('job_source_archive')
    miscellaneous_archive = load_archive('miscellaneous_archive')
    persisted_data_archive = load_archive('persisted_data_archive')

    return PipelineArchiver(job_id, None, persisted_data_archive, None, job_source_archive, artifact_archive, miscellaneous_archive)