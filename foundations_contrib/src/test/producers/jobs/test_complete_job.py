"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_contrib.producers.jobs.complete_job import CompleteJob


class TestProducerCompleteJob(unittest.TestCase):

    def setUp(self):
        from foundations_internal.pipeline_context import PipelineContext

        self.route_name = None
        self.message = None

        self._pipeline_context = PipelineContext()
        self._pipeline_context.file_name = 'some_project'
        self._router = Mock()
        self._router.push_message.side_effect = self._push_message
        self._producer = CompleteJob(self._router, self._pipeline_context)

    def test_push_message_sends_complete_job_message_to_correct_channel(self):
        self._producer.push_message()
        self.assertEqual('complete_job', self.route_name)

    def test_push_message_sends_complete_job_message_with_job_id(self):
        self._pipeline_context.file_name = 'my fantastic job'
        self._producer.push_message()
        self.assertDictContainsSubset({'job_id': 'my fantastic job'}, self.message)

    def test_push_message_sends_complete_job_message_with_job_id_different_job(self):
        self._pipeline_context.file_name = 'neural nets in space!'
        self._producer.push_message()
        self.assertDictContainsSubset({'job_id': 'neural nets in space!'}, self.message)

    def test_push_message_sends_complete_job_message_with_project_name(self):
        self._pipeline_context.provenance.project_name = 'my fantastic job'
        self._producer.push_message()
        self.assertDictContainsSubset({'project_name': 'my fantastic job'}, self.message)

    def test_push_message_sends_complete_job_message_with_project_name_different_job(self):
        self._pipeline_context.provenance.project_name = 'neural nets in space!'
        self._producer.push_message()
        self.assertDictContainsSubset({'project_name': 'neural nets in space!'}, self.message)

    def _push_message(self, route_name, message):
        self.route_name = route_name
        self.message = message
