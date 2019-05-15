"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def load_archive(name):
    from foundations_contrib.global_state import config_manager
    from foundations_contrib.null_archive import NullArchive

    return config_manager.reflect_instance(name, 'archive', lambda: NullArchive())

def get_pipeline_archiver_for_job(job_id):
    from foundations_internal.pipeline_archiver import PipelineArchiver

    artifact_archive = load_archive('artifact_archive')
    job_source_archive = load_archive('job_source_archive')

    return PipelineArchiver(job_id, None, None, None, None, job_source_archive, artifact_archive, None)