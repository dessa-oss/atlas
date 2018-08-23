"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class StateChanger(object):
    """
    Allows for setting, and getting of state of modules
    """
    
    
    def __init__(self, module_name, state_to_change, value):
        self._module = self._load_module(module_name)
        self._state_to_change = state_to_change
        self._value = value
        self._previous_value = None

    def __enter__(self):
        """
        Gets and sets stores attributes for state of modules
        """
        self._previous_value = getattr(self._module, self._state_to_change)
        setattr(self._module, self._state_to_change, self._value)

    def __exit__(self, exception_type, exception_value, traceback):
        """
        Sets attributes for state for state of modules

        Arguments:
            exception_type: Error type
            exception_value: Error value
            traceback: Stack trace from error
        """
        setattr(self._module, self._state_to_change, self._previous_value)

        
    def _load_module(self, module_name):
        module = importlib.import_module(module_name)

        module_components = module_name.split('.')
        for component in module_components[1:]:
            module = getattr(module, component)

        return module