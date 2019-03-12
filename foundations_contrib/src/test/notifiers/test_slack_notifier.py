"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import let, let_patch_mock, let_mock, let_now, set_up
from foundations_spec.helpers.conditional_return import ConditionalReturn
from foundations_spec.helpers.partial_callable_mock import PartialCallableMock

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
    
    @let
    def channel(self):
        return self.faker.name()
    
    mock_slack_client_instance = let_mock()

    @set_up
    def set_up(self):
        self.mock_slack_client = self.patch('slackclient.SlackClient', ConditionalReturn())
        self.mock_slack_client.return_when(self.mock_slack_client_instance, self.token)

    def test_notify_sends_message_to_slack(self):
        self._setup_mock()
        self.notifier.send_message('', self.message)
        self.mock_slack_client_instance.api_call.assert_called_with_partial('chat.postMessage', text=self.message)
    
    def test_notify_does_not_send_message_when_token_is_missing(self):
        del self.os_env['FOUNDATIONS_SLACK_TOKEN']
        self.notifier.send_message('', self.message)
        self.mock_slack_client_instance.api_call.assert_not_called()

    def test_notify_only_creates_one_client(self):
        self._setup_mock()
        self.notifier.send_message('', self.message)
        self.notifier.send_message('', self.message)
        self.mock_slack_client.assert_called_once()
    
    def test_notify_does_not_send_message_channel_is_missing(self):
        self.notifier.send_message(None, self.message)
        self.mock_slack_client_instance.api_call.assert_not_called()
    
    def test_notify_sends_to_correct_channel(self):
        self._setup_mock()
        self.notifier.send_message(self.channel, self.message)
        actual_args, actual_kwargs = self.mock_slack_client_instance.api_call.call_args
        self.mock_slack_client_instance.api_call.assert_called_with_partial('chat.postMessage', channel=self.channel)

    def test_notify_return_true_when_api_call_succeeds(self):
        self._setup_mock()
        self.assertTrue(self.notifier.send_message(self.channel, self.message))

    def test_notify_return_false_when_api_call_fails(self):
        self.mock_slack_client_instance.api_call.return_value = {'ok': False}
        self.assertFalse(self.notifier.send_message(self.channel, self.message))

    def test_notify_return_true_when_token_not_provided(self):
        del self.os_env['FOUNDATIONS_SLACK_TOKEN']
        self.assertTrue(self.notifier.send_message(self.channel, self.message))

    def _setup_mock(self):
        self.mock_slack_client_instance.api_call = PartialCallableMock()
        self.mock_slack_client_instance.api_call.return_value = {'ok': True}