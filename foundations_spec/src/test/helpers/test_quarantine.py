"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_spec import *

class TestQuarantine(unittest.TestCase):

    class MockSpec(Spec):

        @quarantine
        def test_will_throw_assertion_error_if_not_quarantined(self):
            raise AssertionError('test_was_run')

    def setUp(self):
        self._test_case = self.MockSpec()

    def test_run_quarantined_test_method_does_not_actually_run_the_method(self):
        with self.assertWarns(QuarantineWarning):
            self._test_case.test_will_throw_assertion_error_if_not_quarantined()

    def test_run_quarantined_test_method_raises_warning(self):
        with self.assertWarns(QuarantineWarning) as warning:
            self._test_case.test_will_throw_assertion_error_if_not_quarantined()
        
        message = 'TEST "TestQuarantine.MockSpec.test_will_throw_assertion_error_if_not_quarantined" IS QUARANTINED - PLEASE INVESTIGATE ASAP'
        hashes = '#' * len(message)

        self.assertIn(f'\n{hashes}\n\n{message}\n\n{hashes}\n', warning.warning.args)

    def test_quarantine_does_not_change_method_name(self):
        method_name = self._test_case.test_will_throw_assertion_error_if_not_quarantined.__name__
        expected_method_name = 'test_will_throw_assertion_error_if_not_quarantined'

        self.assertEqual(expected_method_name, method_name)

    def test_quarantine_sets_unittest_skip_true(self):
        with self.assertWarns(QuarantineWarning):
            self.assertTrue(self._test_case.test_will_throw_assertion_error_if_not_quarantined.__unittest_skip__)

    def test_quarantine_throws_warning_immediately_if_test_item_is_a_class(self):
        with self.assertWarns(QuarantineWarning) as warning:
            quarantine(self.MockSpec)
        
        message = 'TEST SUITE "TestQuarantine.MockSpec" IS QUARANTINED - PLEASE INVESTIGATE ASAP'
        hashes = '#' * len(message)

        self.assertIn(f'\n{hashes}\n\n{message}\n\n{hashes}\n', warning.warning.args)