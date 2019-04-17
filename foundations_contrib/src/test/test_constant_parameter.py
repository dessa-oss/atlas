"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_contrib.constant_parameter import ConstantParameter
from foundations_contrib.middleware.basic_stage_middleware import BasicStageMiddleware

class TestConstantParameter(Spec):

    class MockClass(object):
        def __str__(self, *args):
            return str(args)
    
    @let
    def fake_arguments(self):
        return tuple(self.faker.words())

    def test_stores_value(self):
        parameter = ConstantParameter('world')
        self.assertEqual('world', parameter.compute_value(None))

    def test_stores_value_different_value(self):
        parameter = ConstantParameter('potato')
        self.assertEqual('potato', parameter.compute_value(None))

    def test_provenance(self):
        parameter = ConstantParameter('world')
        self.assertEqual({'value': 'world', 'type': 'constant'},
                         parameter.provenance())

    def test_provenance_different_value(self):
        parameter = ConstantParameter('potato')
        self.assertEqual(
            {'value': 'potato', 'type': 'constant'}, parameter.provenance())

    def test_value_hash(self):
        parameter = ConstantParameter('potato')
        self.assertEqual(
            '3e2e95f5ad970eadfa7e17eaf73da97024aa5359', parameter.hash(None))

    def test_value_hash_different_value(self):
        parameter = ConstantParameter('mashed potato')
        self.assertEqual(
            '321e42b16eff1d6695a97ed82dc8b24f455db67d', parameter.hash(None))

    def test_has_enable_caching_method(self):
        parameter = ConstantParameter('mashed potato')
        parameter.enable_caching()

    def test_str_returns_underlying_str(self):
        parameter = ConstantParameter('1')
        self.assertEqual('1', str(parameter))

    def test_str_returns_underlying_str_different_value(self):
        parameter = ConstantParameter('hello world')
        self.assertEqual('hello world', str(parameter))
    
    def test_str_supports_passing_arguments(self):
        mock_class = self.MockClass()
        parameter = ConstantParameter(mock_class)
        self.assertEqual(str(self.fake_arguments), parameter.__str__(*self.fake_arguments))