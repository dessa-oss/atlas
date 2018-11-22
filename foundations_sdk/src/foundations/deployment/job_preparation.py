"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class JobPreparation(object):
    
    def __init__(self, message_router, job, job_id):
        self._message_router = message_router
        self._job = job
        self._job_id = job_id

    def prepare(self):
        from foundations.producers.jobs.queue_job import QueueJob

        pipeline_context = self._job.pipeline_context()
        pipeline_context.file_name = self._job_id
        pipeline_context.provenance.job_run_data = self._job.kwargs
        QueueJob(self._message_router, pipeline_context).push_message()
