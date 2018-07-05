"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

import vcat_sdk_fixtures.stage_connector_wrapper_fixtures as scf

class TestStageConnectorWrapper(unittest.TestCase):
    def test_generate_random_params_set_empty_dict(self):
        self.assertEqual({}, scf.DummyConnectorWrapper._generate_random_params_set({}))

    def test_generate_random_params_set_one_entry_one_choice(self):
        for _ in range(10):
            self.assertEqual({'a': 1}, scf.DummyConnectorWrapper._generate_random_params_set(scf.simple_param_set))

    def test_generate_random_params_set_one_entry_two_choices(self):
        import random

        random.seed(2002)

        for _ in range(10):
            random_set = scf.DummyConnectorWrapper._generate_random_params_set(scf.less_simple_param_set)
            self.assertIn(random_set['a'], [1, 2])

        random_set_0 = scf.DummyConnectorWrapper._generate_random_params_set(scf.less_simple_param_set)
        random_set_1 = scf.DummyConnectorWrapper._generate_random_params_set(scf.less_simple_param_set)

        self.assertNotEqual(random_set_0['a'], random_set_1['a'])