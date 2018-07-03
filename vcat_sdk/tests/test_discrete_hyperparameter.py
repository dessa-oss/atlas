"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from vcat.discrete_hyperparameter import DiscreteHyperparameter

class TestDiscreteHyperparameter(unittest.TestCase):
    def test_grid_sample_no_elements(self):
        disc = DiscreteHyperparameter([])
        sample = disc.grid_sample()
        self.assertEqual([], list(sample))

    def test_grid_sample_one_element(self):
        disc = DiscreteHyperparameter([1])
        sample = disc.grid_sample()
        self.assertEqual([1], list(sample))

    def test_random_sample_no_elements(self):
        disc = DiscreteHyperparameter([])
        sample = disc.random_sample()
        for item in sample:
            self.fail("should not be anything in this sample")

    def test_random_sample_one_element_one_time(self):
        disc = DiscreteHyperparameter([1])
        sample = disc.random_sample()
        items = []
        for item in sample:
            if len(items) < 1:
                items.append(item)
            else:
                break

        self.assertEqual(items, [1])

    def test_random_sample_one_element_two_times(self):
        disc = DiscreteHyperparameter([1])
        sample = disc.random_sample()
        items = []
        for item in sample:
            if len(items) < 2:
                items.append(item)
            else:
                break

        self.assertEqual(items, [1] * 2)

    def test_random_sample_two_elements_ten_times(self):
        import random

        disc = DiscreteHyperparameter([1, 2])
        random.seed(1001)

        def generate_random_sample():
            sample = disc.random_sample()
            items = []
            for item in sample:
                if len(items) < 10:
                    items.append(item)
                else:
                    break

            return items

        items0 = generate_random_sample()
        items1 = generate_random_sample()

        self.assertEqual(len(items0), 10)
        self.assertEqual(len(items1), 10)

        for item in items0 + items1:
            self.assertIn(item, [1, 2])

        self.assertNotEqual(items0, items1)