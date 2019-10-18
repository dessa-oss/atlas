"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers.quarantine import quarantine, QuarantineWarning

class TestQuarantine(unittest.TestCase):

    class MockSpec(Spec):
        
        @quarantine
        def test_will_throw_assertion_error_if_not_quarantined(self):
            raise AssertionError('test_was_run')

    def test_run_quarantined_test_method_does_not_actually_run_the_method(self):
        test_case = self.MockSpec()
        test_case.test_will_throw_assertion_error_if_not_quarantined()

    def test_run_quarantined_test_method_raises_warning(self):
        test_case = self.MockSpec()

        with self.assertWarns(QuarantineWarning) as warning:
            test_case.test_will_throw_assertion_error_if_not_quarantined()
        
        self.assertIn('------ test is quarantined - please investigate asap', warning.warning.args)

    