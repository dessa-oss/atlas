"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 02 2019
"""

from foundations_spec import *
from foundations_production.model_package import ModelPackage

class TestModelPackage(Spec):
    
    @let
    def fake_model(self):
        return self.faker.sentence()

    @let
    def fake_preprocessor(self):
        return self.faker.sentence()

    def test_model_package_returns_model(self):
        model_package = ModelPackage(model=self.fake_model, preprocessor=None)
        self.assertEqual(self.fake_model, model_package.model)

    def test_model_package_returns_preprocessor(self):
        model_package = ModelPackage(model=None, preprocessor=self.fake_preprocessor)
        self.assertEqual(self.fake_preprocessor, model_package.preprocessor)