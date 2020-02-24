

class MockMixin(object):

    def _mock_tear_down(self):
        for mock in reversed(self._get_mocks()):
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