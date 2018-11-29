"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, patch

from foundations.deployment.job_preparation import prepare_job

class TestJobPreparation(unittest.TestCase):

    def setUp(self):
        from foundations.pipeline_context import PipelineContext

        self._message_router = Mock()
        self._pipeline_context = PipelineContext()
        self._job = Mock()
        self._job.pipeline_context.return_value = self._pipeline_context
        self._run_data = {'some random data': self._random_uuid()}
        self._job.kwargs = self._run_data
        self._job_id = self._random_uuid()

    def test_prepare_sets_job_id(self):
        prepare_job(self._message_router, self._job, self._job_id)
        self.assertEqual(self._job_id, self._pipeline_context.file_name)

    def test_prepare_sets_run_data(self):
        prepare_job(self._message_router, self._job, self._job_id)
        self.assertEqual(self._job.kwargs, self._pipeline_context.provenance.job_run_data)

    @patch('foundations.producers.jobs.queue_job.QueueJob')
    def test_pushes_queue_message(self, queue_job):
        queue_job_instance = Mock()
        queue_job.return_value = queue_job_instance

        prepare_job(self._message_router, self._job, self._job_id)
        queue_job.assert_called_with(self._message_router, self._pipeline_context)
        queue_job_instance.push_message.assert_called_once()

    def _random_uuid(self):
        from uuid import uuid4
        return str(uuid4())