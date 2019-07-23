"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from test.datetime_faker import fake_current_datetime, restore_real_current_datetime
from foundations_contrib.producers.jobs.queue_job import QueueJob
from foundations_contrib.producers.jobs.run_job import RunJob
from foundations_contrib.producers.jobs.complete_job import CompleteJob


class JobsTestsHelperMixinV2(object):

    @classmethod
    def setUpClass(klass):
        from foundations_contrib.global_state import message_router
        from foundations_internal.pipeline import Pipeline
        from foundations_internal.pipeline_context import PipelineContext

        klass._message_router = message_router
        klass._pipeline_context = PipelineContext()
        klass._pipeline = Pipeline(klass._pipeline_context)

    @classmethod
    def _set_project_name(klass, project_name):
        klass._project_name = project_name
        klass._pipeline_context.provenance.project_name = klass._project_name

    @staticmethod
    def _str_random_uuid():
        import uuid
        return str(uuid.uuid4())

    @staticmethod
    def _fake_start_time(start_timestamp=None):
        if start_timestamp:
            fake_current_datetime(start_timestamp)

    @staticmethod
    def _fake_end_time(end_timestamp=None):
        if end_timestamp:
            fake_current_datetime(end_timestamp)

    @staticmethod
    def _restore_time(start_timestamp=None, end_timestamp=None):
        if start_timestamp or end_timestamp:
            restore_real_current_datetime()

    @classmethod
    def _make_completed_job(klass, job_name, user, tags=None, start_timestamp=None, end_timestamp=None, **kwargs):
        klass._pipeline_context.file_name = job_name
        klass._pipeline_context.provenance.user_name = user
        klass._pipeline_context.provenance.job_run_data = kwargs
        QueueJob(klass._message_router, klass._pipeline_context).push_message()
        klass._fake_start_time(start_timestamp)
        RunJob(klass._message_router, klass._pipeline_context).push_message()
        klass._set_tags(job_name, tags)
        klass._fake_end_time(end_timestamp)
        CompleteJob(klass._message_router, klass._pipeline_context).push_message()
        klass._restore_time(start_timestamp, end_timestamp)

    @classmethod
    def _make_running_job(klass, job_name, user, tags=None, start_timestamp=None):
        klass._pipeline_context.file_name = job_name
        klass._pipeline_context.provenance.user_name = user
        QueueJob(klass._message_router, klass._pipeline_context).push_message()
        klass._fake_start_time(start_timestamp)
        RunJob(klass._message_router, klass._pipeline_context).push_message()
        klass._set_tags(job_name, tags)
        klass._restore_time(start_timestamp, None)

    @classmethod
    def _make_queued_job(klass, job_name, user):
        klass._pipeline_context.file_name = job_name
        klass._pipeline_context.provenance.user_name = user
        QueueJob(klass._message_router, klass._pipeline_context).push_message()

    @classmethod
    def _set_tags(klass, job_name, tags):
        from foundations_contrib.global_state import current_foundations_context
        from foundations import set_tag

        pipeline_context = current_foundations_context().pipeline_context()
        pipeline_context.file_name = job_name

        if tags is not None:
            for key, value in tags.items():
                set_tag(key, value)

        pipeline_context.file_name = None