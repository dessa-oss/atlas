"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class ListParameter(object):

    def __init__(self, list_of_parameters):
        self._list_of_parameters = list_of_parameters

    def compute_value(self, runtime_data):
        return [parameter.compute_value(runtime_data) for parameter in self._list_of_parameters]

    def provenance(self):
        return {'type': 'list', 'parameters': self._list_provenance()}

    def _list_provenance(self):
        return [parameter.provenance() for parameter in self._list_of_parameters]

    def hash(self, runtime_data):
        from foundations.utils import merged_uuids
        return merged_uuids(self._list_hashes(runtime_data))

    def _list_hashes(self, runtime_data):
        return [parameter.hash(runtime_data) for parameter in self._list_of_parameters]

    def enable_caching(self):
        for parameter in self._list_of_parameters:
            parameter.enable_caching()

    def __str__(self):
        return self._list_of_strs().__str__()

    def _list_of_strs(self):
        return [parameter.__str__() for parameter in self._list_of_parameters]
