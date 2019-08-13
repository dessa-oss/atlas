"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestIngressToModelPackage(Spec):

    def test_model_endpoint_is_added_to_yaml(self):
        from foundations_contrib.resources.model_serving.orbit import ingress

        expected_yaml = self._load_yaml('test/fixtures/ingress_resource_with_model.yaml')
        base_yaml = self._load_yaml('test/fixtures/empty_ingress_resource.yaml')
        self.assertEqual(expected_yaml, ingress.set_model_endpoint(base_yaml, 'project', 'model'))

    def _load_yaml(self, filepath):
        import yaml

        with open(filepath, 'r') as stream:
            return yaml.safe_load(stream)