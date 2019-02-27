"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock, call, patch

import foundations_internal
from foundations_contrib.module_controller import ModuleController
from foundations_contrib.obfuscator import Obfuscator
from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let, let_mock, set_up, let_patch_mock


class TestModuleController(Spec):

    @staticmethod
    def _return_generator(input):
        for item in input:
            yield item

    @patch.object(foundations_internal.module_manager.ModuleManager, 'module_directories_and_names')
    def test_bundle_job_adds_modules(self, mock_module_directories_and_names):

        mock_module_directories_and_names.return_value = TestModuleController._return_generator([
            ('fake_module_name', 'fake_module_directory')])
        module_controller = ModuleController()
        module_name, module_directory =  next(module_controller.get_foundations_modules())
        self.assertEqual(module_name, 'fake_module_name')
        self.assertEqual(module_directory, 'fake_module_directory')
