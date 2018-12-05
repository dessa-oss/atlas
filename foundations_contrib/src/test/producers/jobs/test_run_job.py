"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_contrib.producers.jobs.run_job import RunJob


class TestProducerRunJob(unittest.TestCase):

    def setUp(self):
        from foundations_internal.pipeline_context import PipelineContext

        self.route_name = None
        self.message = None

        self._pipeline_context = PipelineContext()
        self._router = Mock()
        self._router.push_message.side_effect = self._push_message
        self._producer = RunJob(self._router, self._pipeline_context)

    def test_push_message_sends_run_job_message_to_correct_channel(self):
        self._producer.push_message()
        self.assertEqual('run_job', self.route_name)

    def test_push_message_sends_run_job_message_with_job_id(self):
        self._pipeline_context.file_name = 'my fantastic job'
        self._pipeline_context.provenance.project_name = 'this project'
        self._producer.push_message()
        self.assertEqual({'job_id': 'my fantastic job',
                          'project_name': 'this project'}, self.message)

    def test_push_message_sends_run_job_message_with_job_id_different_job_different_project(self):
        self._pipeline_context.file_name = 'neural nets in space!'
        self._pipeline_context.provenance.project_name = 'that project'
        self._producer.push_message()
        self.assertEqual({'job_id': 'neural nets in space!',
                          'project_name': 'that project'}, self.message)

    def _push_message(self, route_name, message):
        self.route_name = route_name
        self.message = message
