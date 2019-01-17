"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class DictParameter(object):
    """Represents a python dictionary where the values are themselves parameters.
    This is used to properly dereference any internal parameters that are non-constant
    
    Arguments:
        dict_of_parameters {dict} -- A dictionary mapping keys to parameters
    """

    def __init__(self, dict_of_parameters):
        self._dict_of_parameters = dict_of_parameters

    def compute_value(self, runtime_data):
        """Computes the resolved value of the parameter
        
        Arguments:
            runtime_data {dict} -- Contains the runtime values defined when calling #run on a stage
        
        Returns:
            object -- The result of evaluating the parameter with the given runtime data
        """

        result = {}
        for key, parameter in self._dict_of_parameters.items():
            result[key] = parameter.compute_value(runtime_data)
        return result

    def provenance(self):
        """Provides information about what was used to create this parameter when a job was run
        
        Returns:
            dict -- Contains the information above
        """

        return {'type': 'dict', 'parameters': self._dict_provenance()}

    def _dict_provenance(self):
        result = {}
        for key, parameter in self._dict_of_parameters.items():
            result[key] = parameter.provenance()
        return result

    def hash(self, runtime_data):
        """Computes a reproducible hashing value for this parameter
        
        Arguments:
            runtime_data {dict} -- Contains the runtime values defined when calling #run on a stage
        
        Returns:
            str -- the hashed value as described above
        """

        from foundations.utils import merged_uuids
        return merged_uuids(self._dict_hashes(runtime_data))

    def _dict_hashes(self, runtime_data):
        return [parameter.hash(runtime_data) for parameter in self._dict_of_parameters.values()]

    def enable_caching(self):
        """Enables caching for this parameter so we don't have to evaluate it multiple times
        """

        for parameter in self._dict_of_parameters.values():
            parameter.enable_caching()

    def __str__(self):
        """String representation of the parameter
        
        Returns:
            str -- As above
        """

        return self._dict_of_strs().__str__()

    def _dict_of_strs(self):
        result = {}
        for key, parameter in self._dict_of_parameters.items():
            result[key] = parameter.__str__()
        return result
