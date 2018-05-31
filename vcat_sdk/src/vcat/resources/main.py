from vcat import Job, JobSourceBundle, config_manager

import glob
import yaml
import time
import sys
import dill as pickle


def main():
    job_source_bundle = JobSourceBundle('job', './')

    config = config_manager.config

    job_name = config.get('job_name', 'job')
    job_binary_path = job_name + '.bin'

    with open(job_binary_path, 'rb') as file:
        job = Job.deserialize(file.read())

    pipeline_context = job.pipeline_context()
    global_stage_context = pipeline_context.global_stage_context
    pipeline_context.provenance.config.update(config)
    config = pipeline_context.provenance.config

    pipeline_context.provenance.job_source_bundle = job_source_bundle

    def execute_job():
        try:
            job.run()
            return None
        except Exception as error:
            exception_info = sys.exc_info()
            global_stage_context.add_error_information(exception_info)
            return exception_info
    exception_info = global_stage_context.time_callback(execute_job)

    with open('results.pkl', 'w+b') as file:
        pickle.dump(pipeline_context._context(), file)

    if global_stage_context.error_information is not None:
        raise exception_info[0], exception_info[1], exception_info[2]

if __name__ == "__main__":
    main()
