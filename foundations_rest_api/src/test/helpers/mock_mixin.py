"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class MockMixin(object):

    def tearDown(self):
        for mock in self._get_mocks():
            mock.stop()

    def patch(self, *args, **kwargs):
        from mock import patch

        mock = patch(*args, **kwargs)
        self._get_mocks().append(mock)

        return mock.start()

    def _get_mocks(self):
        if getattr(self, '_mocks', None) is None:
            self._mocks = []
        return self._mocks
