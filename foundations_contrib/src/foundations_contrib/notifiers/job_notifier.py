"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class JobNotifier(object):
    
    def __init__(self, config_manager, slack_notifier):
        self._channel = config_manager.config().get('job_notification_channel')
        self._slack_notifier = slack_notifier

    def send_message(self, message):
        if not self._slack_notifier.send_message(message=message, channel=self._channel):
            if not self._slack_notifier.send_message(message=message, channel=self._channel):
                self._slack_notifier.send_message(message=message, channel=self._channel)
