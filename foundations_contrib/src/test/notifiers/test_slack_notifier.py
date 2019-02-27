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

class TestSlackNotifier(Spec):

    @let
    def notifier(self):
        from foundations_contrib.notifiers.slack_notifier import SlackNotifier
        return SlackNotifier()

    @let
    def message(self):
        return self.faker.sentence()

    @let_now
    def os_env(self):
        environment = {'FOUNDATIONS_SLACK_TOKEN': self.token}
        return self.patch('os.environ', environment)

    @let
    def token(self):
        return self.faker.sha256()
    
    mock_slack_client_instance = let_mock()

    @set_up
    def set_up(self):
        self.mock_slack_client = self.patch('slackclient.SlackClient', ConditionalReturn())
        self.mock_slack_client.return_when(self.mock_slack_client_instance, self.token)

    def test_notify_sends_message_to_slack(self):
        self.notifier.send_message('', self.message)
        self.mock_slack_client_instance.api_call.assert_called_with('chat.postMessage', text=self.message)
    
    def test_notify_does_not_send_message_when_token_is_missing(self):
        del self.os_env['FOUNDATIONS_SLACK_TOKEN']
        self.notifier.send_message(None, self.message)
        self.mock_slack_client_instance.api_call.assert_not_called()


    def _set_up_mocks(self):
        pass

