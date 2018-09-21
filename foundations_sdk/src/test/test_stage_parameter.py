"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.stage_parameter import StageParameter
from foundations.basic_stage_middleware import BasicStageMiddleware


class TestStageParameter(unittest.TestCase):

    class MockStage(object):

        def __init__(self, name=None):
            from uuid import uuid4

            self.cache_enabled = False
            self._uuid = str(uuid4())
            self._name = name

        def enable_caching(self):
            self.cache_enabled = True

        def uuid(self):
            return self._uuid

        def name(self):
            return self._name

    def test_runs_stage(self):
        def method():
            return 5

        parameter = self._make_parameter(method)
        self.assertEqual(5, parameter.compute_value({}))

    def test_runs_stage_different_method(self):
        def method():
            return 17

        parameter = self._make_parameter(method)
        self.assertEqual(17, parameter.compute_value({}))

    def test_runs_stage_dynamic_parameters(self):
        from foundations.hyperparameter import Hyperparameter

        def method(some_number):
            return 3 * some_number

        parameter = self._make_parameter(method, Hyperparameter('some_number'))
        self.assertEqual(15, parameter.compute_value({'some_number': 5}))

    def test_value_hash(self):
        def method():
            return 'potato'

        parameter = self._make_parameter(method)
        self.assertEqual(
            '3e2e95f5ad970eadfa7e17eaf73da97024aa5359', parameter.hash({}))

    def test_value_hash_different_value(self):
        def method():
            return 'mashed potato'

        parameter = self._make_parameter(method)
        self.assertEqual(
            '321e42b16eff1d6695a97ed82dc8b24f455db67d', parameter.hash({}))

    def test_value_hash_dynamic_value(self):
        from foundations.hyperparameter import Hyperparameter

        def method(some_number):
            return 'hello' * some_number

        parameter = self._make_parameter(method, Hyperparameter('some_number'))
        self.assertEqual('0b156215b189103c3d268f61299a854cd0b31e70',
                         parameter.hash({'some_number': 2}))

    def test_value_hash_dynamic_value_different_value(self):
        from foundations.hyperparameter import Hyperparameter

        def method(some_number):
            return 'hello' * some_number

        parameter = self._make_parameter(method, Hyperparameter('some_number'))
        self.assertEqual('9bbc253eb8d8abfb4dd4a1726cc94892b930b188',
                         parameter.hash({'some_number': 33}))

    def test_enable_caching_forwards_to_stage(self):
        stage = self.MockStage()
        parameter = StageParameter(stage)
        parameter.enable_caching()

        self.assertTrue(stage.cache_enabled)

    def test_provenance_returns_name(self):
        stage = self.MockStage('potato')
        parameter = StageParameter(stage)

        self.assertEqual({'type': 'stage', 'stage_name': 'potato', 'stage_uuid': stage.uuid()}, parameter.provenance())

    def test_provenance_returns_name_different_value(self):
        stage = self.MockStage('tomako')
        parameter = StageParameter(stage)

        self.assertEqual({'type': 'stage', 'stage_name': 'tomako', 'stage_uuid': stage.uuid()}, parameter.provenance())

    def test_str_returns_stage_and_name(self):
        stage = self.MockStage()

        parameter = StageParameter(stage)
        expected_string = 'stage::{}'.format(stage.uuid())
        self.assertEqual(expected_string, str(parameter))

    def _make_parameter(self, method, *args):
        from foundations.pipeline import Pipeline
        from foundations.pipeline_context import PipelineContext

        stage = Pipeline(PipelineContext()).stage(method, *args)
        return StageParameter(stage)

