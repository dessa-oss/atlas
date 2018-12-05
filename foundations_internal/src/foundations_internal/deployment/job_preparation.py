"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def prepare_job(message_router, job, job_id):
    from foundations_contrib.producers.jobs.queue_job import QueueJob

    pipeline_context = job.pipeline_context()
    pipeline_context.file_name = job_id
    pipeline_context.provenance.job_run_data = job.kwargs
    QueueJob(message_router, pipeline_context).push_message()
