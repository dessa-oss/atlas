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

    @let
    def is_default(self):
        return self.faker.boolean()

    @let
    def activated_status(self):
        if self.faker.boolean():
            return 'activated'
        return 'deactivated'

    @let
    def created_by(self):
        return self.faker.first_name()

    @let
    def created_at(self):
        return str(self.faker.date_time_this_year())

    def test_has_model_name(self):
        model = Model(model_name=self.model_name)
        self.assertEqual(self.model_name, model.model_name)

    def test_has_default_status(self):
        model = Model(default=self.is_default)
        self.assertEqual(self.is_default, model.default)

    def test_has_activated_status(self):
        model = Model(status=self.activated_status)
        self.assertEqual(self.activated_status, model.status)

    def test_has_created_by(self):
        model = Model(created_by=self.created_by)
        self.assertEqual(self.created_by, model.created_by)
    
    def test_has_created_at(self):
        model = Model(created_at=self.created_at)
        self.assertEqual(self.created_at, model.created_at)
        