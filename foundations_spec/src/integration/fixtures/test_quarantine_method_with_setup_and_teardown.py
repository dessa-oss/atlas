from foundations_spec import *

class TestQuarantineMethod(Spec):

    @set_up
    def set_up(self):
        raise AssertionError('setup ran')

    @tear_down
    def tear_down(self):
        raise AssertionError('teardown ran')

    @quarantine
    def test_should_not_actually_run(self):
        pass