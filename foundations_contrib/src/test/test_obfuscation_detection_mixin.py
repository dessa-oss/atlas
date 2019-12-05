"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import unittest
from mock import Mock, call, patch

from foundations_contrib.obfuscation_detection_mixin import ObfuscationDetectionMixin
from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import let, let_mock, set_up, let_patch_mock


class TestObfuscationDetectionMixin(Spec):

    class MockClassUsingMixin(ObfuscationDetectionMixin):

        def __init__(self, config):
            self._config = config

    @let
    def default_config(self):
        from foundations_contrib.local_shell_job_deployment import LocalShellJobDeployment
        return {
            'obfuscate_foundations': False,
            'deployment_implementation': {
                'deployment_type': LocalShellJobDeployment
            }
        }

    def test_detect_obfuscation_returns_false_when_obfuscation_false(self):
        config = self.default_config
        class_using_mixin = self.MockClassUsingMixin(config)
        self.assertFalse(class_using_mixin.is_obfuscation_activated())


    def test_detect_obfuscation_returns_true_when_obfuscation_true_and_deployment_not_local(self):
        config = self.default_config
        config['obfuscate_foundations'] = True
        config['deployment_implementation']['deployment_type'] = 'whatever'
        class_using_mixin = self.MockClassUsingMixin(config)
        self.assertTrue(class_using_mixin.is_obfuscation_activated())
    
    def test_detect_obfuscation_returns_false_when_obfuscation_false_and_deployment_not_local(self):
        config = self.default_config
        config['obfuscate_foundations'] = False
        config['deployment_implementation']['deployment_type'] = 'whatever'
        class_using_mixin = self.MockClassUsingMixin(config)
        self.assertFalse(class_using_mixin.is_obfuscation_activated())

    def test_detect_obfuscation_returns_false_when_deployment_local(self):
        config = self.default_config
        config['obfuscate_foundations'] = True
        class_using_mixin = self.MockClassUsingMixin(config)
        self.assertFalse(class_using_mixin.is_obfuscation_activated())
