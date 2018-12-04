"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.consumers.jobs.queued.mixins.serialized_parameter import SerializedParameter


class ErrorData(SerializedParameter):
    """Save the parameter used when calling #run on a stage
    to redis

    Arguments:
        redis {redis.Redis} -- A Redis connection
        serializer {object} -- A serializer having a #dumps method to convert the data into a string
    """

    def _get_attribute(self, message):
        return message['error_information']

    def _get_attribute_key(self):
        return 'error_information'
