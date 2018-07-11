"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from vcat.floating_hyperparameter import FloatingHyperparameter

class TestFloatingHyperparameter(unittest.TestCase):
    def test_grid_sample_one_element(self):
        hype = FloatingHyperparameter(min=0, max=0, step=0.1)
        sample = hype.grid_elements()
        self.assertEqual([0], sample)

    def test_grid_sample_three_elements(self):
        hype = FloatingHyperparameter(min=0.1, max=1.2, step=0.4)
        sample = hype.grid_elements()
        self.assertEqual([0.1, 0.5, 0.9], sample)

    def test_step_should_not_be_zero_for_grid_search(self):
        try:
            hype = FloatingHyperparameter(min=0, max=1, step=0)
            hype.grid_elements()
            self.fail("this should not have succeeded")
        except ValueError:
            pass

    def test_step_should_not_be_none_for_grid_search(self):
        try:
            hype = FloatingHyperparameter(min=0, max=1)
            hype.grid_elements()
            self.fail("this should not have succeeded")
        except TypeError:
            pass

    def test_random_sample_one_point(self):
        hype = FloatingHyperparameter(min=0, max=0)

        for _ in range(20):
            self.assertEqual(0, hype.random_sample())

    def test_random_sample_range(self):
        import random

        from vcat_sdk_helpers.floating_hyperparameter_helpers import make_unique_and_sorted

        hype = FloatingHyperparameter(min=0.1, max=0.2)

        random.seed(20002)
        samples = [hype.random_sample() for _ in range(20)]

        samples.sort()

        self.assertEqual(make_unique_and_sorted(samples), samples)
