"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class MockMixin(object):

    def setUp(self):
        self._mocks = []

    def testDown(self):
        for mock in self._mocks:
            mock.stop()

    def patch(self, *args, **kwargs):
        from mock import patch

        mock = patch(*args, **kwargs)
        self._mocks.append(mock)

        return mock.start()
