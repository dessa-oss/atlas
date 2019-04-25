"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from foundations_spec import *

from foundations_production import model

class TestModelDecorator(Spec):

    mock_callback = let_mock()
    mock_preprocessor_class = let_patch_mock('foundations_production.preprocessor_class.Preprocessor')

    def test_model_decorator_takes_callback_and_constructs_preprocessor_that_uses_callback(self):
        model(self.mock_callback)
        self.mock_preprocessor_class.assert_called_with(self.mock_callback, "model")

    def test_model_decorator_takes_callback_and_returns_preprocessor_that_uses_callback(self):
        self.assertIs(self.mock_preprocessor_class.return_value, model(self.mock_callback))
