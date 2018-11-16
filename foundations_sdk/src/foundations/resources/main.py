"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import sys

from foundations import Job, JobSourceBundle, JobPersister, config_manager, compat_raise, serialize_to_file, log_manager
from foundations.error_printer import ErrorPrinter

def main():
    log = log_manager.get_logger(__name__)
    job_source_bundle = JobSourceBundle('job', './')

    config_manager.freeze()
    config = config_manager.config()

    def set_recursion_limit_if_necessary():
        if 'recursion_limit' in config:
            new_limit = config['recursion_limit']
            log.debug('Overriding recursion limit to {}'.format(new_limit))
            sys.setrecursionlimit(new_limit)
    set_recursion_limit_if_necessary()

    job_name = config.get('job_name', 'job')
    job_binary_path = job_name + '.bin'

    log.debug('Running job {} with configuration {}'.format(job_name, config))

    with open(job_binary_path, 'rb') as file:
        job = Job.deserialize(file.read())

    pipeline_context = job.pipeline_context()
    pipeline_context.mark_fully_loaded()
    pipeline_context.file_name = job_name
    global_stage_context = pipeline_context.global_stage_context
    pipeline_context.fill_provenance(config_manager)
    config = pipeline_context.provenance.config

    pipeline_context.provenance.job_source_bundle = job_source_bundle

    def fetch_error_information(context):
        import sys
        exception_info = sys.exc_info()
        context.global_stage_context.add_error_information(exception_info)
        return exception_info

    def mark_job_complete():
        from foundations.producers.jobs.complete_job import CompleteJob
        from foundations.global_state import message_router

        CompleteJob(message_router, job.pipeline_context()).push_message()

    def execute_job():
        try:
            job.run()
            mark_job_complete()
            return None, False
        except Exception as error:
            return fetch_error_information(pipeline_context), True
    exception_info, was_job_error = global_stage_context.time_callback(execute_job)

    def save_context(context):
        with open('results.pkl', 'w+b') as file:
            serialize_to_file(context._context(), file)

    def serialize_job_results(exception_info, was_job_error):
        try:
            JobPersister(job).persist()

            save_context(pipeline_context)
            return exception_info, was_job_error
        except Exception as error:
            from foundations.pipeline_context import PipelineContext

            error_pipeline_context = PipelineContext()

            exception_info = fetch_error_information(error_pipeline_context)
            save_context(error_pipeline_context)

            return exception_info, False

    exception_info, was_job_error = serialize_job_results(exception_info, was_job_error)

    if exception_info is not None:
        if not was_job_error:
            sys.excepthook = sys.__excepthook__
        
        compat_raise(exception_info[0], exception_info[1], exception_info[2])

if __name__ == "__main__":
    main()
