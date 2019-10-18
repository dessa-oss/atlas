from foundations_spec import *

@quarantine
class TestQuarantineClass(Spec):

    @set_up_class
    def set_up_class(cls):
        raise AssertionError('setupclass ran')

    @tear_down_class
    def tear_down(cls):
        raise AssertionError('teardownclass ran')

    def test_should_not_actually_run(self):
        raise AssertionError('method ran')