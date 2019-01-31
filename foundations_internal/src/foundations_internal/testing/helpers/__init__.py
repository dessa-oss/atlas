"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Callback(object):
    def __init__(self, function):
        self._function = function

    def __call__(self, *args, **kwargs):
        return self._function(*args, **kwargs)

class set_up(Callback):
    pass 

class tear_down(Callback):
    pass 

class let(Callback):
    pass

def let_mock():
    from mock import Mock
    
    def _callback(self):
        return Mock()
    
    return let(_callback)