"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class JobNotifier(object):
    
    def __init__(self, config_manager, slack_notifier):
        self._slack_notifier = slack_notifier
        self._config_manager = config_manager

    def send_message(self, message):
        channel = self._get_channel()
        for _ in range(5):
            if self._slack_notifier.send_message(message=message, channel=channel):
                break

    def _get_channel(self):
        return self._config_manager.config().get('job_notification_channel')