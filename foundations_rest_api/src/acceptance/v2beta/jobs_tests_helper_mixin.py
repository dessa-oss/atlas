"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from foundations.producers.jobs.queue_job import QueueJob
from foundations.producers.jobs.run_job import RunJob
from foundations.producers.jobs.complete_job import CompleteJob

class JobsTestsHelperMixin(object):

    @classmethod
    def setUpClass(klass):
        from foundations.global_state import message_router
        from foundations.pipeline import Pipeline
        from foundations.pipeline_context import PipelineContext

        klass._message_router = message_router
        klass._pipeline_context = PipelineContext()
        klass._pipeline = Pipeline(klass._pipeline_context)

    @staticmethod
    def _str_random_uuid():
        import uuid
        return str(uuid.uuid4())

    @classmethod
    def _make_completed_job(klass, job_name, user):
        klass._pipeline_context.file_name = job_name
        klass._pipeline_context.provenance.user_name = user
        QueueJob(klass._message_router, klass._pipeline_context).push_message()
        RunJob(klass._message_router, klass._pipeline_context).push_message()
        CompleteJob(klass._message_router, klass._pipeline_context).push_message()

    @classmethod
    def _make_running_job(klass, job_name, user):
        klass._pipeline_context.file_name = job_name
        klass._pipeline_context.provenance.user_name = user
        QueueJob(klass._message_router, klass._pipeline_context).push_message()
        RunJob(klass._message_router, klass._pipeline_context).push_message()

    @classmethod
    def _make_queued_job(klass, job_name, user):
        klass._pipeline_context.file_name = job_name
        klass._pipeline_context.provenance.user_name = user
        QueueJob(klass._message_router, klass._pipeline_context).push_message()
