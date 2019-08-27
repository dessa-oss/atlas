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
    mock_manifest = let_mock()
    mock_path_exists = let_patch_mock_with_conditional_return('os.path.exists')
    mock_manifest_validator_class = let_patch_mock_with_conditional_return('foundations_model_package.manifest_validator.ManifestValidator')
    mock_manifest_validator = Mock()

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

        self.mock_file.__enter__ = self._mock_enter
        self.mock_file.__exit__ = self._mock_exit

        self.mock_path_exists.return_when(True, self.manifest_path)

        self.mock_manifest_validator_class.return_when(self.mock_manifest_validator, self.mock_manifest)

        self.mock_yaml_load.return_when(self.mock_manifest, self.mock_file)

    def test_id_returns_id_from_environment(self):
        job = Job(self.job_id)
        self.assertEqual(self.job_id, job.id())

    def test_root_returns_path_to_job_archive_on_disk(self):
        job = Job(self.job_id)
        self.assertEqual(self.job_root, job.root())

    def test_manifest_returns_parsed_output_from_yaml_file(self):
        job = Job(self.job_id)
        self.assertEqual(self.mock_manifest, job.manifest())

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

    def test_manifest_validator_called_when_loading_manifest(self):
        self.mock_manifest_validator.validate_manifest.reset_mock()

        job = Job(self.job_id)
        job.manifest()

        self.mock_manifest_validator.validate_manifest.assert_called_once()

    def test_manifest_does_not_reload_manifest_if_already_loaded(self):
        job = Job(self.job_id)
        job.manifest()
        job.manifest()

        self.mock_open.assert_called_once()

    def test_manifest_does_not_check_whether_manifest_path_exists_if_already_loaded(self):
        job = Job(self.job_id)
        job.manifest()
        job.manifest()

        self.mock_path_exists.assert_called_once()

    def _mock_enter(self, *args, **kwargs):
        return self.mock_file

    def _mock_exit(self, *args, **kwargs):
        pass