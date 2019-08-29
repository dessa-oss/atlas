"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Foundations Team <pairing@dessa.com>, 06 2018
"""

def deploy(project_name, entrypoint, params):
    import os
    import os.path as path
    import json

    from foundations_contrib.job_deployer import deploy_job
    from foundations_contrib.global_state import current_foundations_context, redis_connection, config_manager
    from foundations_internal.pipeline_context_wrapper import PipelineContextWrapper

    if project_name is None:
        project_name = path.basename(os.getcwd())

    current_foundations_context().set_project_name(project_name)
    config_manager['run_script_environment'] = {'script_to_run': entrypoint or 'main.py', 'enable_stages': False}
    
    pipeline_context_wrapper = PipelineContextWrapper(current_foundations_context().pipeline_context())

    if params is not None:
        with open('foundations_job_parameters.json', 'w+') as params_file:
            json.dump(params, params_file)

    return deploy_job(pipeline_context_wrapper, None, {})