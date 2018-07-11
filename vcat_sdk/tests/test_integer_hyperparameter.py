"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from vcat.integer_hyperparameter import IntegerHyperparameter

class TestIntegerHyperparameter(unittest.TestCase):
    def test_grid_sample_no_elements(self):
        hype = IntegerHyperparameter(start=0, stop=0)
        sample = hype.grid_elements()
        self.assertEqual([], sample)

    def test_grid_sample_one_element(self):
        hype = IntegerHyperparameter(start=0, stop=1)
        sample = hype.grid_elements()
        self.assertEqual([0], sample)

    def test_grid_sample_three_elements(self):
        hype = IntegerHyperparameter(start=0, stop=7, step=3)
        sample = hype.grid_elements()
        self.assertEqual([0, 3, 6], sample)

    def test_random_sample_no_elements(self):
        hype = IntegerHyperparameter(start=10, stop=10)
        try:
            sample = hype.random_sample()
            self.fail("should not be anything in this sample")
        except ValueError:
            pass

    def test_random_sample_one_element_one_time(self):
        hype = IntegerHyperparameter(start=0, stop=1)
        for _ in range(1):
            self.assertEqual(0, hype.random_sample())

    def test_random_sample_one_element_two_times(self):
        hype = IntegerHyperparameter(start=0, stop=1)
        for _ in range(2):
            self.assertEqual(0, hype.random_sample())

    def test_random_sample_three_elements_ten_times(self):
        import random

        hype = IntegerHyperparameter(start=10, stop=111, step=50)
        random.seed(1001)

        def generate_random_sample():
            return [hype.random_sample() for _ in range(10)]

        items0 = generate_random_sample()
        items1 = generate_random_sample()

        for item in items0 + items1:
            self.assertIn(item, [10, 60, 110])

        self.assertNotEqual(items0, items1)