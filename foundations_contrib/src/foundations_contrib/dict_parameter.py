"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class DictParameter(object):

    def __init__(self, dict_of_parameters):
        self._dict_of_parameters = dict_of_parameters

    def compute_value(self, runtime_data):
        result = {}
        for key, parameter in self._dict_of_parameters.items():
            result[key] = parameter.compute_value(runtime_data)
        return result

    def provenance(self):
        return {'type': 'dict', 'parameters': self._dict_provenance()}

    def _dict_provenance(self):
        result = {}
        for key, parameter in self._dict_of_parameters.items():
            result[key] = parameter.provenance()
        return result

    def hash(self, runtime_data):
        from foundations.utils import merged_uuids
        return merged_uuids(self._dict_hashes(runtime_data))

    def _dict_hashes(self, runtime_data):
        return [parameter.hash(runtime_data) for parameter in self._dict_of_parameters.values()]

    def enable_caching(self):
        for parameter in self._dict_of_parameters.values():
            parameter.enable_caching()

    def __str__(self):
        return self._dict_of_strs().__str__()

    def _dict_of_strs(self):
        result = {}
        for key, parameter in self._dict_of_parameters.items():
            result[key] = parameter.__str__()
        return result
