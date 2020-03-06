from foundations_spec import *

class TestQuarantineMethod(Spec):

    @quarantine
    def test_should_not_actually_run(self):
        raise AssertionError('i ran but should not have')