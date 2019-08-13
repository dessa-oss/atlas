"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def load_local_configuration_if_present():
    from foundations.config import set_environment
    from foundations_contrib.global_state import current_foundations_context, message_router
    from foundations_contrib.producers.jobs.queue_job import QueueJob
    from foundations_contrib.producers.jobs.run_job import RunJob
    import atexit

    if _default_environment_present():
        set_environment('default')
        pipeline_context = current_foundations_context().pipeline_context()
        _set_job_state(pipeline_context)
        QueueJob(message_router, pipeline_context).push_message()
        RunJob(message_router, pipeline_context).push_message()
        atexit.register(_at_exit_callback)

def _at_exit_callback():
    from foundations_contrib.global_state import current_foundations_context
    from foundations_contrib.archiving.upload_artifacts import upload_artifacts
    
    pipeline_context = current_foundations_context().pipeline_context()
    upload_artifacts(pipeline_context.job_id)
        
def _set_job_state(pipeline_context):
    from uuid import uuid4

    pipeline_context.file_name = str(uuid4())
    pipeline_context.provenance.project_name = _default_project_name()

def _default_project_name():
    import os
    import os.path

    return os.path.basename(os.getcwd())
        
def _default_environment_present():
    from os.path import basename

    environments = _environment_listing()
    environments = [basename(path) for path in environments]
    return 'default.config.yaml' in environments

def _environment_listing():
    from foundations_contrib.cli.environment_fetcher import EnvironmentFetcher
            
    environment_fetcher = EnvironmentFetcher()
    local_environments, global_environments = environment_fetcher.get_all_environments()
    local_environments = local_environments or []
    global_environments = global_environments or []

    return local_environments + global_environments