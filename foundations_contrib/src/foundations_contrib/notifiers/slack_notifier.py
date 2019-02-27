"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class SlackNotifier(object):

    def __init__(self):
        self._slack_client = self._create_client()
    
    def send_message(self, channel, message):
        if self._slack_client is not None and channel is not None:
            self._slack_client.api_call('chat.postMessage', text=message)

    @staticmethod
    def _create_client():
        from slackclient import SlackClient
        import os

        slack_token = os.environ.get('FOUNDATIONS_SLACK_TOKEN')
        if slack_token is not None:
            return SlackClient(slack_token)
