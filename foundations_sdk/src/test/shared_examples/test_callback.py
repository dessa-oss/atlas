"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class TestCallback(object):

    def _callback(self, args, kwargs):
        from uuid import uuid4

        self._called_callback = True
        self._callback_args = args
        self._callback_kwargs = kwargs

        if not hasattr(self, '_callback_result'):
            self._callback_result = uuid4()
        return self._callback_result
