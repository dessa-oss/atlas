"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let, let_patch_mock, let_mock, let_now, set_up
from foundations_internal.testing.helpers.conditional_return import ConditionalReturn
from foundations_internal.testing.helpers.partial_callable_mock import PartialCallableMock

class TestJobNotifier(Spec):
    
    @let
    def channel(self):
        return self.faker.name()

    @let
    def message(self):
        return self.faker.sentence()

    @let
    def config_manager(self):
        from foundations.config_manager import ConfigManager
        return ConfigManager()
    
    slack_notifier = let_mock()

    @let
    def notifier(self):
        from foundations_contrib.notifiers.job_notifier import JobNotifier
        return JobNotifier(self.config_manager, self.slack_notifier)

    def test_sends_message_to_slack_notifier(self):
        self.slack_notifier.send_message = PartialCallableMock()
        self.notifier.send_message(self.message)
        self.slack_notifier.send_message.assert_called_with_partial(message=self.message)

    def test_sends_null_channel_if_not_defined(self):
        self.slack_notifier.send_message = PartialCallableMock()
        self.notifier.send_message(self.message)
        self.slack_notifier.send_message.assert_called_with_partial(channel=None)

    def test_uses_channel_in_config(self):
        self.config_manager['job_notification_channel'] = self.channel
        self.slack_notifier.send_message = PartialCallableMock()
        self.notifier.send_message(self.message)
        self.slack_notifier.send_message.assert_called_with_partial(channel=self.channel)