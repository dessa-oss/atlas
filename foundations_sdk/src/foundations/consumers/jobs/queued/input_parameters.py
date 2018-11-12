"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.consumers.jobs.queued.mixins.serialized_parameter import SerializedParameter

class InputParameters(SerializedParameter):
    """Stores information about the input parameters used to create each
    parameter for a Foundations stage
    
    Arguments:
        redis {redis.Redis} -- A Redis connection object
        serializer {object} -- A serializer having a #dumps method to convert the data into a string
    """
    
    def _get_attribute(self, message):
        return message['input_parameters']

    def _get_attribute_key(self):
        return 'input_parameters'