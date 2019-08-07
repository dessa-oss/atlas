"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_model_package.job import Job

class TestJob(Spec):

    mock_open = let_patch_mock_with_conditional_return('builtins.open')
    mock_file = let_mock()
    mock_yaml_load = let_patch_mock_with_conditional_return('yaml.load')
    mock_path_exists = let_patch_mock_with_conditional_return('os.path.exists')

    @let
    def module_name(self):
        return self.faker.word()

    @let
    def function_name(self):
        return self.faker.word()

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def job_root(self):
        return f'/archive/archive/{self.job_id}/artifacts'

    @set_up
    def set_up(self):
        self.manifest_path = f'{self.job_root}/foundations_package_manifest.yaml'
        self.mock_open.return_when(self.mock_file, self.manifest_path, 'r')

        self.mock_path_exists.return_when(True, self.manifest_path)

        self.mock_file.__enter__ = self._mock_enter
        self.mock_file.__exit__ = self._mock_exit

    def test_id_returns_id_from_environment(self):
        job = Job(self.job_id)
        self.assertEqual(self.job_id, job.id())

    def test_root_returns_path_to_job_archive_on_disk(self):
        job = Job(self.job_id)
        self.assertEqual(self.job_root, job.root())

    def test_manifest_returns_parsed_output_from_yaml_file(self):
        loaded_yaml = {
            'entrypoints': {
                'predict': {
                    'module': self.module_name,
                    'function': self.function_name
                }
            }
        }

        self.mock_yaml_load.return_when(loaded_yaml, self.mock_file)

        job = Job(self.job_id)
        self.assertEqual(loaded_yaml, job.manifest())

    def test_manifest_raises_exception_if_file_does_not_exist(self):
        self.mock_path_exists.clear()
        self.mock_path_exists.return_when(False, self.manifest_path)
        
        job = Job(self.job_id)
        
        with self.assertRaises(Exception) as error_context:
            job.manifest()
        
        self.assertIn('Manifest file, foundations_package_manifest.yaml not found!', error_context.exception.args)

    def test_manifest_raises_exception_if_yaml_file_is_invalid(self):
        self.mock_yaml_load = self.patch('yaml.load')

        import yaml

        self.mock_yaml_load.side_effect = yaml.parser.ParserError()

        job = Job(self.job_id)

        with self.assertRaises(Exception) as error_context:
            job.manifest()

        self.assertIn('Manifest file was not a valid YAML file!', error_context.exception.args)

    def test_manifest_raises_exception_if_prediction_module_name_missing(self):
        loaded_yaml = {
            'entrypoints': {
                'predict': {
                    'function': self.function_name
                }
            }
        }
        self.mock_yaml_load.return_when(loaded_yaml, self.mock_file)

        job = Job(self.job_id)

        with self.assertRaises(Exception) as error_context:
            job.manifest()

        self.assertIn('Prediction module name missing from manifest file!', error_context.exception.args)

    def test_manifest_raises_exception_if_prediction_function_name_missing(self):
        loaded_yaml = {
            'entrypoints': {
                'predict': {
                    'module': self.module_name
                }
            }
        }
        self.mock_yaml_load.return_when(loaded_yaml, self.mock_file)

        job = Job(self.job_id)

        with self.assertRaises(Exception) as error_context:
            job.manifest()

        self.assertIn('Prediction function name missing from manifest file!', error_context.exception.args)

    def test_manifest_raises_exception_if_predict_entrypoint_is_missing(self):
        loaded_yaml = {
            'entrypoints': {}
        }
        self.mock_yaml_load.return_when(loaded_yaml, self.mock_file)

        job = Job(self.job_id)

        with self.assertRaises(Exception) as error_context:
            job.manifest()

        self.assertIn('Prediction entrypoint missing from manifest file!', error_context.exception.args)

    def test_manifest_raises_exception_if_entrypoints_section_is_missing(self):
        loaded_yaml = {}
        self.mock_yaml_load.return_when(loaded_yaml, self.mock_file)

        job = Job(self.job_id)

        with self.assertRaises(Exception) as error_context:
            job.manifest()

        self.assertIn('Entrypoints section missing from manifest file!', error_context.exception.args)

    def _mock_enter(self, *args, **kwargs):
        return self.mock_file

    def _mock_exit(self, *args, **kwargs):
        pass