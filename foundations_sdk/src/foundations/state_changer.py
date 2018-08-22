"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class StateChanger(object):
    
    def __init__(self, state_to_change, value):
        self._state_to_change = state_to_change
        self._value = value
        self._previous_value = None

    def __enter__(self):
        import foundations

        self._previous_value = getattr(foundations, self._state_to_change)
        setattr(foundations, self._state_to_change, self._value)

    def __exit__(self, exception_type, exception_value, traceback):
        import foundations
        setattr(foundations, self._state_to_change, self._previous_value)
        
