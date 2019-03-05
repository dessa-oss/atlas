"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Katherine Bancroft <k.bancroft@dessa.com>, 06 2018
"""


from foundations_contrib.global_state import config_manager

config_manager['job_notification_channel'] = 'spamity'
config_manager['job_notification_channel_id'] = 'CFNA44YRJ'

import foundations

from integration.test_consumers import TestConsumers
from integration.test_consumer_compatibility import TestConsumerCompatibility
