
class MockDeployment(object):

    def __init__(self, scheduler_backend_callback):
        self._scheduler_backend_callback = scheduler_backend_callback

    def scheduler_backend(self):
        return self._scheduler_backend_callback
