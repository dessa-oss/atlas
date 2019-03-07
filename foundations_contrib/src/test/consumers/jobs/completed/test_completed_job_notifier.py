"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_internal.testing.helpers import *
from foundations_internal.testing.helpers.spec import Spec

class TestCompletedJobNotifier(Spec):

    job_notifier = let_mock()

    @let
    def consumer(self):
        from foundations_contrib.consumers.jobs.completed.job_notifier import JobNotifier
        return JobNotifier(self.job_notifier)

    @let
    def job_id(self):
        from uuid import uuid4
        return uuid4()

    @let
    def project_name(self):
        return self.faker.sentence()

    def test_call_sends_notification_with_qeueud_message(self):
        time = 1551457960.22515
        self.consumer.call({'job_id': self.job_id, 'project_name': self.project_name}, time, None)
        self.job_notifier.send_message.assert_called_with(
            """
Job Completed
Job Id: {}
Timestamp: 2019-03-01 11:32:40.225150
Project Name: {}
            """.format(self.job_id, self.project_name)
        )


    def test_call_sends_notification_with_qeueud_message_different_time_stamp(self):
        time = 1551458381.9642663
        self.consumer.call({'job_id': self.job_id, 'project_name': self.project_name}, time, None)
        self.job_notifier.send_message.assert_called_with(
            """
Job Completed
Job Id: {}
Timestamp: 2019-03-01 11:39:41.964266
Project Name: {}
            """.format(self.job_id, self.project_name)
        )