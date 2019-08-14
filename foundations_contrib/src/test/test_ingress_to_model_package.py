"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_contrib.resources.model_serving.orbit import ingress

class TestIngressToModelPackage(Spec):

    def test_model_endpoint_is_added_to_yaml_if_project_default_already_exists(self):
        expected_yaml = self._load_yaml('test/fixtures/ingress_resource_with_model_and_default_project.yaml')
        base_yaml = self._load_yaml('test/fixtures/ingress_resource_with_default.yaml')

        self.assertEqual(expected_yaml, ingress.set_model_endpoint(base_yaml, 'project', 'model'))
    
    def test_default_project_and_model_endpoint_created_when_first_model_created_within_project(self):
        expected_yaml = self._load_yaml('test/fixtures/ingress_resource_with_model_and_default_project.yaml')
        base_yaml = self._load_yaml('test/fixtures/empty_ingress_resource.yaml')

        self.assertEqual(expected_yaml, ingress.set_model_endpoint(base_yaml, 'project', 'model'))
    
    def test_default_project_not_clobbered_when_already_set_and_new_model_added_to_project(self):
        expected_yaml = self._load_yaml('test/fixtures/ingress_resource_with_two_models_and_default_project.yaml')
        base_yaml = self._load_yaml('test/fixtures/ingress_resource_with_default_project_and_model.yaml')

        self.assertEqual(expected_yaml, ingress.set_model_endpoint(base_yaml, 'project', 'model-two'))

    def _load_yaml(self, filepath):
        import yaml

        with open(filepath, 'r') as stream:
            return yaml.safe_load(stream)