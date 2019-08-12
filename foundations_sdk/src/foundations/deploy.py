"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Foundations Team <pairing@dessa.com>, 06 2018
"""

def deploy(project_name=None, env='local', entrypoint='main.py', job_directory=None, params=None):
    import os
    import os.path as path
    import json

    import foundations
    from foundations.job_deployer import deploy_job
    from foundations_contrib.global_state import current_foundations_context, redis_connection
    from foundations_internal.pipeline_context_wrapper import PipelineContextWrapper

    _log_job_deployed(project_name, env, entrypoint, job_directory, params)

    cwd_path = os.getcwd()

    if job_directory is not None:
        os.chdir(job_directory)
        target_directory = job_directory
    else:
        target_directory = cwd_path

    if project_name is None:
        project_name = path.basename(target_directory)

    foundations.set_project_name(project_name)
    foundations.set_environment(env)
    redis_connection.incr('foundations:sdk:deloyment_count')
    foundations.config_manager['run_script_environment'] = {'script_to_run': entrypoint, 'enable_stages': False}
    
    pipeline_context_wrapper = PipelineContextWrapper(current_foundations_context().pipeline_context())

    if params is not None:
        with open('foundations_job_parameters.json', 'w') as params_file:
            json.dump(params, params_file)

    job_deployment = deploy_job(pipeline_context_wrapper, None, {})

    if job_directory is not None:
        os.chdir(cwd_path)

    return job_deployment

def _log_job_deployed(project_name, env, entrypoint, job_directory, params):
    from foundations_contrib.global_state import message_router

    message = {
        'project_name': project_name, 
        'environment': env, 
        'entrypoint': entrypoint, 
        'job_directory': job_directory, 
        'params': params
    }
    message_router.push_message('job_deployed_with_sdk', message)
