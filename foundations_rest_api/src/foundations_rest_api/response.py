"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class Response(object):

    def __init__(self, resource_name, action_callback, parent=None):
        self._action_callback = action_callback
        self._parent = parent

    def evaluate(self):
        if self._parent is not None:
            self._parent.evaluate()
        return self._action_callback()
