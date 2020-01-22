"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_orbit.contract_validators.domain_checker import DomainChecker

from hypothesis import given
import hypothesis.strategies as st
from hypothesis.extra.pandas import column, columns, data_frames
import numpy as np
import pandas as pd

@skip('Not Implemented')
class TestDomainChecker(Spec):
    def test_validate_with_no_columns_configured_returns_empty_results(self):
        expected_result = {
            'summary': {
                'healthy': 0,
                'critical': 0,
                'warning': 0
            },
            'details_by_attribute': []
        }
        self.assertEqual(expected_result, DomainChecker().validate())
