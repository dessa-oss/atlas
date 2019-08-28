"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_model_package.resource_factories import retrain_resource

class TestRetrainResource(Spec):
    
    @let
    def module_name(self):
        return self.faker.word()

    @let
    def function_name(self):
        return self.faker.word()

    def test_retrain_resource_is_instance_of_flask_restful_resource(self):
        from flask_restful import Resource

        resource_class = retrain_resource(self.module_name, self.function_name)
        resource = resource_class()
        self.assertIsInstance(resource, Resource)