"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

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

    def test_run_quarantined_test_method_does_not_actually_run_the_method(self):
        self.test_case_class().test_will_throw_assertion_error_if_not_quarantined()

    def test_run_quarantined_method_results_in_exithook_registered_that_throws_error_message(self):
        self.test_case_class
        
        with self.assertWarns(QuarantineWarning) as warning:
            self.register.execute()
        
        message = 'TEST "TestQuarantine.test_case_class.<locals>.MockSpec.test_will_throw_assertion_error_if_not_quarantined" IS QUARANTINED - PLEASE INVESTIGATE ASAP'
        hashes = '#' * len(message)

        self.assertIn(f'\n{hashes}\n\n{message}\n\n{hashes}\n', warning.warning.args)

    def test_quarantine_does_not_change_method_name(self):
        method_name = self.test_case_class().test_will_throw_assertion_error_if_not_quarantined.__name__
        expected_method_name = 'test_will_throw_assertion_error_if_not_quarantined'

        self.assertEqual(expected_method_name, method_name)

    def test_quarantine_sets_unittest_skip_true(self):
        test_case = self.test_case_class()
        self.assertTrue(test_case.test_will_throw_assertion_error_if_not_quarantined.__unittest_skip__)

    def test_quarantine_throws_warning_if_test_item_is_a_class(self):
        self.quarantined_class
        
        with self.assertWarns(QuarantineWarning) as warning:
            self.register.execute()
        
        message = 'TEST SUITE "TestQuarantine.quarantined_class.<locals>.QuarantinedSpec" IS QUARANTINED - PLEASE INVESTIGATE ASAP'
        hashes = '#' * len(message)

        self.assertIn(f'\n{hashes}\n\n{message}\n\n{hashes}\n', warning.warning.args)

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