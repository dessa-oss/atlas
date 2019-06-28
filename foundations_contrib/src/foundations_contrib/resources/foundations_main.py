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
from foundations_internal.compat import compat_raise
from foundations_contrib.global_state import foundations_context
from foundations_contrib.archiving.upload_artifacts import upload_artifacts

def set_recursion_limit_if_necessary(config, log):
    if 'recursion_limit' in config:
        new_limit = config['recursion_limit']
        log.debug('Overriding recursion limit to {}'.format(new_limit))
        sys.setrecursionlimit(new_limit)

def mark_job_failed(job):
    from foundations_contrib.producers.jobs.failed_job import FailedJob
    from foundations.global_state import message_router

    job_pipeline_context = job.pipeline_context()
    job_error_information = job_pipeline_context.global_stage_context.error_information
    FailedJob(message_router, job_pipeline_context,
                job_error_information).push_message()

def fetch_error_information(context, job):
    import sys
    exception_info = sys.exc_info()
    context.global_stage_context.add_error_information(exception_info)
    mark_job_failed(job)
    return exception_info

def mark_job_complete(job):
    from foundations_contrib.producers.jobs.complete_job import CompleteJob
    from foundations.global_state import message_router

    CompleteJob(message_router, job.pipeline_context()).push_message()

def mark_job_as_running(job):
    from foundations_contrib.producers.jobs.run_job import RunJob
    from foundations.global_state import message_router

    RunJob(message_router, job.pipeline_context()).push_message()

def execute_job(job, pipeline_context):
    try:
        mark_job_as_running(job)
        run_job_variant(job)
        mark_job_complete(job)
        return None, False
    except Exception as error:
        return fetch_error_information(pipeline_context, job), True

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

def save_context(context):
    with open('results.pkl', 'w+b') as file:
        serialize_to_file(context._context(), file)

def serialize_job_results(exception_info, was_job_error, job, pipeline_context):
    try:
        JobPersister(job).persist()

        save_context(pipeline_context)
        return exception_info, was_job_error
    except Exception as error:
        from foundations_internal.pipeline_context import PipelineContext

        error_pipeline_context = PipelineContext()

        exception_info = fetch_error_information(error_pipeline_context, job)
        save_context(error_pipeline_context)

        return exception_info, False

def initialize_pipeline_context(job, job_name, job_source_bundle):
    pipeline_context = job.pipeline_context()
    pipeline_context.mark_fully_loaded()
    pipeline_context.file_name = job_name
    pipeline_context.fill_provenance(config_manager)
    pipeline_context.provenance.job_source_bundle = job_source_bundle

    return pipeline_context

def main():
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

    exception_info, was_job_error = global_stage_context.time_callback(lambda: execute_job(job, pipeline_context))
    upload_artifacts(job_name)

    exception_info, was_job_error = serialize_job_results(exception_info, was_job_error, job, pipeline_context)

    if exception_info is not None:
        if not was_job_error:
            sys.excepthook = sys.__excepthook__

        compat_raise(exception_info[0], exception_info[1], exception_info[2])

if __name__ == "__main__":
    main()
