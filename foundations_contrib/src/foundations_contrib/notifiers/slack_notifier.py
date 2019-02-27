"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class SlackNotifier(object):
    
    def send_message(self, channel, message):
        from slackclient import SlackClient
        import os

        slack_token = os.environ.get('FOUNDATIONS_SLACK_TOKEN')
        if slack_token is not None:
            slackclient = SlackClient(slack_token)
            slackclient.api_call('chat.postMessage', text=message)