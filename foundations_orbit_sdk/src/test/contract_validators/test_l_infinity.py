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

    @let
    def element_1(self):
        import numpy
        return self.faker.random.randint(1, 100)

    @let
    def element_2(self):
        import numpy
        return self.faker.random.randint(1, 100)

    @let
    def array_1(self):
        import numpy
        return numpy.array([self.element_1])

    @let
    def array_2(self):
        import numpy
        return numpy.array([self.element_2])

    @let
    def array_1_length_2(self):
        import numpy
        return numpy.array([0, 5])

    @let
    def array_2_length_2(self):
        import numpy
        return numpy.array([0, 1])

    def test_l_infinity_raises_value_error_if_both_arrays_are_empty(self):
        with self.assertRaises(ValueError) as ex:
            l_infinity(self.empty_array, self.empty_array)

        self.assertIn('cannot take l_infinity distance of empty arrays', ex.exception.args)

    def test_l_infinity_returns_l_infinity_of_difference_between_two_vectors_of_length_1(self):
        import numpy

        l_infinity_value = l_infinity(self.array_1, self.array_2)
        expected_value = numpy.abs(self.element_1 - self.element_2)
        self.assertEqual(expected_value, l_infinity_value)

    def test_l_infinity_returns_l_infinity_of_difference_between_two_vectors_of_length_2(self):
        import numpy

        l_infinity_value = l_infinity(self.array_1_length_2, self.array_2_length_2)
        self.assertEqual(4, l_infinity_value)
