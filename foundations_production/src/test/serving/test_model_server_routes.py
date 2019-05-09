"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

import unittest
from mock import Mock

from foundations_spec.helpers import let, let_now, let_patch_mock, set_up
from foundations_spec.helpers.spec import Spec
from flask import Flask

class TestModelServerRoutes(Spec):
    
    @set_up
    def set_up(self):
        from foundations_production.serving.model_server_routes import load_routes

        self.app = Flask(__name__)
        load_routes(self.app)

    def test_manage_model_package_route_is_added(self):
        self.assertIn('manage_model_package', self.app.view_functions)

    def test_training_all_model_packages_route_is_added(self):
        self.assertIn('train_all_model_packages', self.app.view_functions)

    def test_training_one_model_package_route_is_added(self):
        self.assertIn('train_one_model_package', self.app.view_functions)

    def test_predictions_from_model_package_route_is_added(self):
        self.assertIn('predictions_from_model_package', self.app.view_functions)

    def test_predict_with_model_package_route_is_added(self):
        self.assertIn('predict_with_model_package', self.app.view_functions)