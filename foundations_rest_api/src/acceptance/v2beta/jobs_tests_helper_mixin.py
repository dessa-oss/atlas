"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from foundations_contrib.producers.jobs.queue_job import QueueJob
from foundations_contrib.producers.jobs.run_job import RunJob
from foundations_contrib.producers.jobs.complete_job import CompleteJob


class JobsTestsHelperMixin(object):

    def setUp(self):
        from foundations.global_state import message_router
        from foundations.global_state import redis_connection
        from foundations_internal.pipeline import Pipeline
        from foundations_internal.pipeline_context import PipelineContext

        redis_connection.flushall()

        self._message_router = message_router
        self._pipeline_context = PipelineContext()
        self._pipeline = Pipeline(self._pipeline_context)

    @staticmethod
    def _str_random_uuid():
        import uuid
        return str(uuid.uuid4())

    def _make_completed_job(self, job_name, user):
        self._pipeline_context.file_name = job_name
        self._pipeline_context.provenance.user_name = user
        QueueJob(self._message_router, self._pipeline_context).push_message()
        RunJob(self._message_router, self._pipeline_context).push_message()
        CompleteJob(self._message_router,
                    self._pipeline_context).push_message()

    def _make_running_job(self, job_name, user):
        self._pipeline_context.file_name = job_name
        self._pipeline_context.provenance.user_name = user
        QueueJob(self._message_router, self._pipeline_context).push_message()
        RunJob(self._message_router, self._pipeline_context).push_message()

    def _make_queued_job(self, job_name, user):
        self._pipeline_context.file_name = job_name
        self._pipeline_context.provenance.user_name = user
        QueueJob(self._message_router, self._pipeline_context).push_message()

    def _assert_list_contains_items(self, expected, result):
        for item in expected:
            if not item in result:
                self.fail('Element {} not found in {}'.format(item, result))

