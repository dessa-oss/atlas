"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def save_artifact(filepath):
    from foundations_contrib.global_state import log_manager, current_foundations_context
    from foundations_contrib.archiving import load_archive

    logger = log_manager.get_logger(__name__)
    foundations_context = current_foundations_context()

    if not foundations_context.is_in_running_job():
        logger.warning('Cannot save artifact outside of job.')
    else:
        job_id = foundations_context.job_id()
        artifact_archive = load_archive('artifact_archive')
        artifact_archive.append_file('artifacts', filepath, job_id)