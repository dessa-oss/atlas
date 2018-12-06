"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.consumers.jobs.queued.mixins.attribute_key_list import AttributeKeyList


class InputParameterKeys(AttributeKeyList):
    """Stores a list of all common stage input parameter keys for a project in redis

    Arguments:
        redis {redis.Redis} -- A Redis connection object
    """

    def _get_attribute(self, message):
        import time, json
        parameter_list = message['input_parameters']
        parameters = {}
        for parameter in parameter_list:
            stage_uuid = parameter['stage_uuid']
            parameter_name = parameter['argument']['name']
            parameter_value = parameter['argument']['value']
            key = json.dumps({'parameter_name': parameter_name,
                              'stage_uuid': stage_uuid,
                              'time': time.time()})
            parameters[key] = parameter_value
        return parameters

    def _get_attribute_key(self):
        return 'input_parameter_names'
