"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.consumers.jobs.queued.mixins.attribute_key_list import AttributeKeyList
import time, json


class StageTime(AttributeKeyList):
    """Stores a list of all common stage input parameter keys for a project in redis

    Arguments:
        redis {redis.Redis} -- A Redis connection object
    """

    def _get_attribute(self, message):   
        parameter_list = message['input_parameters']
        parameters = {}
        for parameter in parameter_list:
            self._add_stage_uuid_from_stage(parameter, parameters)

            if parameter['argument']['value']['type'] == 'stage':
                self._add_stage_uuid_from_stage_with_no_input_params(parameter, parameters)
        return parameters

    def _get_attribute_key(self):
        return 'stage_time'

    def _add_stage_uuid_from_stage_with_no_input_params(self, parameter, parameters):
        stage_uuid = parameter['argument']['value']['stage_uuid']
        key = json.dumps({'stage_uuid': stage_uuid,
            'time': time.time()})
        parameters[key] = 'no_param_stage'
    
    def _add_stage_uuid_from_stage(self, parameter, parameters):
        stage_uuid = parameter['stage_uuid']
        parameter_value = parameter['argument']['value']
        key = json.dumps({'stage_uuid': stage_uuid,
                            'time': time.time()})
        parameters[key] = parameter_value
