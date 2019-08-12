"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.v1.models.model import Model

class TestModel(Spec):

    @let
    def model_name(self):
        return self.faker.word()

    def test_has_model_name(self):
        model = Model(model_name=self.model_name)
        self.assertEqual(self.model_name, model.model_name)