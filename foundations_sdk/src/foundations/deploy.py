"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Foundations Team <pairing@dessa.com>, 06 2018
"""

def deploy(project_name=None, env='local', entrypoint='main.py', job_directory=None):
    import os
    import os.path as path

    import foundations
    from foundations.job_deployer import deploy_job
    from foundations_contrib.global_state import current_foundations_context
    from foundations_internal.pipeline_context_wrapper import PipelineContextWrapper

    cwd_path = os.getcwd()

    if project_name is None:
        project_name = path.basename(cwd_path)

    foundations.set_project_name(project_name)
    foundations.set_environment(env)
    foundations.config_manager['run_script_environment'] = {'script_to_run': entrypoint, 'enable_stages': False}
    
    pipeline_context_wrapper = PipelineContextWrapper(current_foundations_context().pipeline_context())

    os.chdir(job_directory)
    deploy_job(pipeline_context_wrapper, None, {})
    os.chdir(cwd_path)