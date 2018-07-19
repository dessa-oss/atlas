"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from vcat import *


class TestPlaceHolderParameters(unittest.TestCase):

    def test_can_replace_input(self):
        def method(value):
            return value
        stage = pipeline.stage(method, Hyperparameter("value"))
        self.assertEqual(9, stage.run_same_process(value=9))

    def test_can_replace_input_with_different_name(self):
        def method(value):
            return value
        stage = pipeline.stage(method, Hyperparameter("special_value"))
        self.assertEqual(9, stage.run_same_process(special_value=9))

    def test_can_replace_keyword_parameter(self):
        def method(value):
            return value
        stage = pipeline.stage(method, value=Hyperparameter())
        self.assertEqual(9, stage.run_same_process(value=9))

    def test_can_replace_multiple_parameters(self):
        def method(value, value2):
            return value + value2
        stage = pipeline.stage(method, value=Hyperparameter(), value2=Hyperparameter())
        self.assertEqual(4, stage.run_same_process(value=1, value2=3))

    def test_can_replace_multiple_parameters_same_placeholder(self):
        def method(value, value2):
            return value + value2
        param = Hyperparameter("input")
        stage = pipeline.stage(method, param, param)
        self.assertEqual(4, stage.run_same_process(input=2))

    def test_can_mix_with_normal_parameters(self):
        def method(value, value2):
            return value + value2
        param = Hyperparameter("input")
        stage = pipeline.stage(method, param, 3)
        self.assertEqual(5, stage.run_same_process(input=2))

    def test_supports_deep_placeholders(self):
        def make_value(value):
            return value

        def scale(value, scale):
            return value * scale

        stage = pipeline.stage(make_value, Hyperparameter("input"))
        stage2 = pipeline.stage(scale, stage, Hyperparameter("scale"))
        self.assertEqual(18, stage2.run_same_process(input=2, scale=9))
