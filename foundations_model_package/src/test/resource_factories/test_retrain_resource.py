"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_model_package.resource_factories import retrain_resource

class TestRetrainResource(Spec):
    
    mock_retrain_driver = let_mock()

    @let
    def retrain_driver_path(self):
        return self.faker.file_path()

    @set_up
    def set_up(self):
        self.mock_retrain_driver.__enter__ = lambda *args: self.retrain_driver_path
        self.mock_retrain_driver.__exit__ = lambda *args: None

    def test_retrain_resource_is_instance_of_flask_restful_resource(self):
        from flask_restful import Resource

        resource_class = retrain_resource(self.mock_retrain_driver)
        resource = resource_class()
        self.assertIsInstance(resource, Resource)

    def test_retrain_resource_has_different_name_each_time_when_constructed(self):
        resource_class_0 = retrain_resource(self.mock_retrain_driver)
        resource_class_1 = retrain_resource(self.mock_retrain_driver)

        self.assertNotEqual(resource_class_0.__name__, resource_class_1.__name__)