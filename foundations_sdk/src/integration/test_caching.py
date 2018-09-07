"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations.global_state import foundations_context


class TestCaching(unittest.TestCase):

    def test_local_caching(self):
        self.value = 3

        def method():
            self.value = self.value * 2

        stage = foundations_context.pipeline().stage(method)
        stage.run_same_process()
        stage.run_same_process()
        self.assertEqual(6, self.value)

    def test_simple_cross_stage_caching(self):
        self.value = 3

        def method():
            self.value = self.value * 2

        stage = foundations_context.pipeline().stage(method).enable_caching()
        stage.run_same_process()
        
        stage2 = foundations_context.pipeline().stage(method).enable_caching()
        stage2.run_same_process()
        self.assertEqual(6, self.value)

    def test_cross_stage_caching_returns_expected_value(self):
        def method():
            from random import randint
            return randint(1, 1000)

        stage = foundations_context.pipeline().stage(method).enable_caching()
        expected_value = stage.run_same_process()
        
        stage2 = foundations_context.pipeline().stage(method).enable_caching()
        result = stage2.run_same_process()
        self.assertEqual(expected_value, result)

    def test_split_stage_caching(self):
        def method():
            from random import randint
            return [randint(1, 1000)]

        stage = foundations_context.pipeline().stage(method)
        split_stage, = stage.split(1)
        split_stage.enable_caching()
        expected_value = split_stage.run_same_process()
        
        stage2 = foundations_context.pipeline().stage(method)
        split_stage2, = stage2.split(1)
        split_stage2.enable_caching()
        result = split_stage2.run_same_process()
        self.assertEqual(expected_value, result)
