"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class GlobalMetricLogger(object):
    
    def log_metric(self, key, value):
        from foundations_contrib.global_state import log_manager

        logger = log_manager.get_logger(__name__)
        logger.warning('Cannot log metric if not deployed with foundations deploy')