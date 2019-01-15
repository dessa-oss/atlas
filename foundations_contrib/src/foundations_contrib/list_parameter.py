"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class ListParameter(object):
    """Represents a python list where the values are themselves parameters.
    This is used to properly dereference any internal parameters that are non-constant
    
    Arguments:
        list_of_parameters {dict} -- A list of parameters
    """

    def __init__(self, list_of_parameters):
        self._list_of_parameters = list_of_parameters

    def compute_value(self, runtime_data):
        """Computes the resolved value of the parameter
        
        Arguments:
            runtime_data {dict} -- Contains the runtime values defined when calling #run on a stage
        
        Returns:
            object -- The result of evaluating the parameter with the given runtime data
        """

        return [parameter.compute_value(runtime_data) for parameter in self._list_of_parameters]

    def provenance(self):
        """Provides information about what was used to create this parameter when a job was run
        
        Returns:
            dict -- Contains the information above
        """

        return {'type': 'list', 'parameters': self._list_provenance()}

    def _list_provenance(self):
        return [parameter.provenance() for parameter in self._list_of_parameters]

    def hash(self, runtime_data):
        """Computes a reproducible hashing value for this parameter
        
        Arguments:
            runtime_data {dict} -- Contains the runtime values defined when calling #run on a stage
        
        Returns:
            str -- the hashed value as described above
        """

        from foundations.utils import merged_uuids
        return merged_uuids(self._list_hashes(runtime_data))

    def _list_hashes(self, runtime_data):
        return [parameter.hash(runtime_data) for parameter in self._list_of_parameters]

    def enable_caching(self):
        """Enables caching for this parameter so we don't have to evaluate it multiple times
        """

        for parameter in self._list_of_parameters:
            parameter.enable_caching()

    def __str__(self):
        """String representation of the parameter
        
        Returns:
            str -- As above
        """

        return self._list_of_strs().__str__()

    def _list_of_strs(self):
        return [parameter.__str__() for parameter in self._list_of_parameters]
