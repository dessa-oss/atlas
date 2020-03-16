
from foundations_spec import *

class TestQuarantine(Spec):

    @let_now
    def register(self):
        return self.patch('atexit.register', _MockRegister())

    @let
    def test_case_class(self):
        class MockSpec(Spec):

            @quarantine
            def test_will_throw_assertion_error_if_not_quarantined(self):
                raise AssertionError('should not have been executed!')

        return MockSpec

    @let
    def quarantined_class(self):
        @quarantine
        class QuarantinedSpec(Spec):

            def test_will_throw_assertion_error_if_not_quarantined(self):
                raise AssertionError('should not have been executed!')
        
        return QuarantinedSpec

    @let
    def test_case_class_multiple_quarantines(self):
        class MockSpecMultiple(Spec):

            @quarantine
            def test_first_method(self):
                raise AssertionError('should not have been executed!')

            @quarantine
            def test_second_method(self):
                raise AssertionError('should not have been executed!')

        return MockSpecMultiple

    @let
    def QuarantineWarning(self):
        from foundations_spec.helpers.quarantine import QuarantineWarning
        return QuarantineWarning

    @set_up
    def set_up(self):
        import importlib
        import foundations_spec.helpers.quarantine as quarantine
        importlib.reload(quarantine)

    def test_run_quarantined_test_method_does_not_actually_run_the_method(self):
        self.test_case_class().test_will_throw_assertion_error_if_not_quarantined()

    def test_run_quarantined_method_results_in_exithook_registered_that_throws_error_message(self):
        self.test_case_class
        
        with self.assertWarns(self.QuarantineWarning) as warning:
            self.register.execute()
        
        message_header = 'THE FOLLOWING ITEMS ARE QUARANTINED; PLEASE INVESTIGATE ASAP:\n'
        message = '\nTestQuarantine.test_case_class.<locals>.MockSpec.test_will_throw_assertion_error_if_not_quarantined'
        hashes = '#' * len(message[1:])

        self.assertEqual(f'\n{hashes}\n\n{message_header + message}\n\n{hashes}\n', warning.warning.args[0])

    def test_quarantine_does_not_change_method_name(self):
        method_name = self.test_case_class().test_will_throw_assertion_error_if_not_quarantined.__name__
        expected_method_name = 'test_will_throw_assertion_error_if_not_quarantined'

        self.assertEqual(expected_method_name, method_name)

    def test_quarantine_sets_unittest_skip_true(self):
        test_case = self.test_case_class()
        self.assertTrue(test_case.test_will_throw_assertion_error_if_not_quarantined.__unittest_skip__)

    def test_quarantine_throws_warning_if_test_item_is_a_class(self):
        self.quarantined_class
        
        with self.assertWarns(self.QuarantineWarning) as warning:
            self.register.execute()
        
        message_header = 'THE FOLLOWING ITEMS ARE QUARANTINED; PLEASE INVESTIGATE ASAP:\n'
        message = '\nTestQuarantine.quarantined_class.<locals>.QuarantinedSpec'
        hashes = '#' * len(message_header[:-1])

        self.assertEqual(f'\n{hashes}\n\n{message_header + message}\n\n{hashes}\n', warning.warning.args[0])

    def test_quarantine_throws_multiple_warnings_in_same_error_block_if_multiple_items_quarantined(self):
        self.test_case_class_multiple_quarantines
        
        with self.assertWarns(self.QuarantineWarning) as warning:
            self.register.execute()
        
        message_header = 'THE FOLLOWING ITEMS ARE QUARANTINED; PLEASE INVESTIGATE ASAP:\n'
        message_0 = '\nTestQuarantine.test_case_class_multiple_quarantines.<locals>.MockSpecMultiple.test_first_method'
        message_1 = '\nTestQuarantine.test_case_class_multiple_quarantines.<locals>.MockSpecMultiple.test_second_method'
        hashes = '#' * len(message_1[1:])

        self.assertEqual(f'\n{hashes}\n\n{message_header + message_0 + message_1}\n\n{hashes}\n', warning.warning.args[0])

class _MockRegister(object):

    def __init__(self):
        self._callback = None
        self._args = None
        self._kwargs = None

    def __call__(self, callback, *args, **kwargs):
        self._callback = callback
        self._args = args
        self._kwargs = kwargs

    def execute(self):
        if self._callback is not None:
            self._callback(*self._args, **self._kwargs)