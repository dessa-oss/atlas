"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.discrete_hyperparameter import DiscreteHyperparameter

class TestDiscreteHyperparameter(unittest.TestCase):
    def test_grid_sample_no_elements(self):
        disc = DiscreteHyperparameter([])
        sample = disc.grid_elements()
        self.assertEqual([], sample)

    def test_grid_sample_one_element(self):
        disc = DiscreteHyperparameter([1])
        sample = disc.grid_elements()
        self.assertEqual([1], sample)

    def test_grid_sample_two_elements(self):
        disc = DiscreteHyperparameter([1, 2])
        sample = disc.grid_elements()
        self.assertEqual([1, 2], sample)

    def test_random_sample_no_elements(self):
        disc = DiscreteHyperparameter([])
        try:
            sample = disc.random_sample()
            self.fail("should not be anything in this sample")
        except ValueError:
            pass

    def test_random_sample_one_element_one_time(self):
        disc = DiscreteHyperparameter([1])
        for _ in range(1):
            self.assertEqual(1, disc.random_sample())

    def test_random_sample_one_element_two_times(self):
        disc = DiscreteHyperparameter([1])
        for _ in range(2):
            self.assertEqual(1, disc.random_sample())

    def test_random_sample_two_elements_ten_times(self):
        import random

        disc = DiscreteHyperparameter([1, 2])
        random.seed(1001)

        def generate_random_sample():
            return [disc.random_sample() for _ in range(10)]

        items0 = generate_random_sample()
        items1 = generate_random_sample()

        for item in items0 + items1:
            self.assertIn(item, [1, 2])

        self.assertNotEqual(items0, items1)