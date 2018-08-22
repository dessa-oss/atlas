"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class StageLoggingContext(object):
    
    def __init__(self, logger):
        self._logger = logger

    def log_metric(self, key, value):
        self._logger.log_metric(key, value)
