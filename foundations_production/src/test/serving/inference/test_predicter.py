"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""


from foundations_spec import *
from foundations_production.serving.inference.predicter import Predicter

class TestPredicter(Spec):

    model_package = let_mock()

    @let
    def predicter(self):
        return Predicter(self.model_package)
    
    def test_predicters_with_same_model_package_are_the_same_predicter(self):
        rhs = Predicter(self.model_package)
        self.assertEqual(rhs, self.predicter)

    def test_predicters_with_diff_model_package_are_diff_predicters(self):
        rhs_model_package = Mock()
        rhs = Predicter(rhs_model_package)
        self.assertNotEqual(rhs, self.predicter)