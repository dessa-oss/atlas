"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import sys

from foundations import Job, JobPersister, config_manager, log_manager, message_router
from foundations_internal.error_printer import ErrorPrinter
from foundations_contrib.job_source_bundle import JobSourceBundle
from foundations_internal.serializer import serialize_to_file
from foundations_contrib.global_state import foundations_context
from foundations_contrib.archiving.upload_artifacts import upload_artifacts

def ensure_configured():
    from foundations.local_run.initialize_default_environment import create_config_file
    from foundations.local_run import set_up_default_environment_if_present

    create_config_file()
    set_up_default_environment_if_present()

def set_recursion_limit_if_necessary(config, log):
    if 'recursion_limit' in config:
        new_limit = config['recursion_limit']
        log.debug('Overriding recursion limit to {}'.format(new_limit))
        sys.setrecursionlimit(new_limit)

def get_user_script_module_and_path(user_script):
    import os
    dirname = os.path.dirname(user_script)

    if dirname:
        user_script = os.path.basename(user_script)
        path = os.path.join(os.getcwd(), dirname)
    else:
        path = os.getcwd()

    module_name = user_script.split('.')[0]
    return module_name, path

def run_user_script(job):
    import os
    from importlib import import_module

    path_to_script = os.environ['script_to_run']
    module_name, path_to_add = get_user_script_module_and_path(path_to_script)
    sys.path.append(path_to_add)
    import_module(module_name)

def run_job_variant(job):
    import os

    if os.environ['enable_stages'] == 'True':
        job.run()
    else:
        run_user_script(job)

def initialize_pipeline_context(job, job_name, job_source_bundle):
    pipeline_context = job.pipeline_context()
    pipeline_context.mark_fully_loaded()
    pipeline_context.file_name = job_name
    pipeline_context.fill_provenance(config_manager)
    pipeline_context.provenance.job_source_bundle = job_source_bundle

    return pipeline_context

def main():
    from foundations_contrib.change_directory import ChangeDirectory
    import os
    import sys

    ensure_configured()

    sys.path.append(os.getcwd() + '/job_source')

    log = log_manager.get_logger(__name__)
    job_source_bundle = JobSourceBundle('job', './')

    config_manager.freeze()
    config = config_manager.config()

    set_recursion_limit_if_necessary(config, log)

    job_name = config.get('job_name', 'job')
    job_binary_path = job_name + '.bin'

    log.debug('Running job {} with configuration {}'.format(job_name, config))

    with open(job_binary_path, 'rb') as file:
        job = Job.deserialize(file.read())

    pipeline_context = initialize_pipeline_context(job, job_name, job_source_bundle)
    config = pipeline_context.provenance.config

    global_stage_context = pipeline_context.global_stage_context
    foundations_context.pipeline()._pipeline_context = pipeline_context

    os.chdir('job_source')
    global_stage_context.time_callback(lambda: run_job_variant(job))

if __name__ == "__main__":
    main()
