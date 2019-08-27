"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_model_package.manifest_validator import ManifestValidator

class TestManifestValidator(Spec):

    @let
    def module_name(self):
        return self.faker.word()

    @let
    def function_name(self):
        return self.faker.word()

    def test_validate_manifest_raises_exception_if_prediction_module_name_missing(self):
        manifest = {
            'entrypoints': {
                'predict': {
                    'function': self.function_name
                }
            }
        }

        with self.assertRaises(Exception) as error_context:
            ManifestValidator(manifest).validate_manifest()

        self.assertIn('Prediction module name missing from manifest file!', error_context.exception.args)

    def test_validate_manifest_raises_exception_if_prediction_function_name_missing(self):
        manifest = {
            'entrypoints': {
                'predict': {
                    'module': self.module_name
                }
            }
        }

        with self.assertRaises(Exception) as error_context:
            ManifestValidator(manifest).validate_manifest()

        self.assertIn('Prediction function name missing from manifest file!', error_context.exception.args)

    def test_validate_manifest_raises_exception_if_predict_entrypoint_is_missing(self):
        manifest = {
            'entrypoints': {}
        }

        with self.assertRaises(Exception) as error_context:
            ManifestValidator(manifest).validate_manifest()

        self.assertIn('Prediction entrypoint missing from manifest file!', error_context.exception.args)

    def test_validate_manifest_raises_exception_if_entrypoints_section_is_missing(self):
        manifest = {}

        with self.assertRaises(Exception) as error_context:
            ManifestValidator(manifest).validate_manifest()

        self.assertIn('Entrypoints section missing from manifest file!', error_context.exception.args)