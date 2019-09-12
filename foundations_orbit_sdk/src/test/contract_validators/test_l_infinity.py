"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit.contract_validators.statistics import l_infinity

class TestLInfinity(Spec):

    @let
    def empty_array(self):
        import numpy
        return numpy.array([])

    def test_l_infinity_raises_value_error_if_both_arrays_are_empty(self):
        with self.assertRaises(ValueError) as ex:
            l_infinity(self.empty_array, self.empty_array)

        self.assertIn('cannot take l_infinity distance of empty arrays', ex.exception.args)
