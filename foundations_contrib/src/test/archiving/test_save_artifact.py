"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_contrib.archiving.save_artifact import save_artifact

class TestSaveArtifact(Spec):

    @let
    def mock_logger(self):
        return Mock()

    @let
    def filepath(self):
        return self.faker.file_path()

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def key(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        mock_get_logger = self.patch('foundations_contrib.global_state.log_manager.get_logger', ConditionalReturn())
        mock_get_logger.return_when(self.mock_logger, 'foundations_contrib.archiving.save_artifact')

        self._mock_foundations_context = Mock()
        mock_foundations_context_function = self.patch('foundations_contrib.global_state.current_foundations_context')

        mock_foundations_context_function.return_value = self._mock_foundations_context

        self._mock_archive = Mock()
        load_archive = self.patch('foundations_contrib.archiving.load_archive', ConditionalReturn())
        load_archive.return_when(self._mock_archive, 'artifact_archive')

        self._mock_archive.exists.return_value = False

    def test_save_artifact_outside_job_logs_warning(self):
        self._mock_foundations_context.is_in_running_job.return_value = False

        save_artifact(self.filepath)
        self.mock_logger.warning.assert_called_once_with('Cannot save artifact outside of job.')

    def test_save_artifact_in_job_does_not_log_warning(self):
        self._mock_foundations_context.is_in_running_job.return_value = True

        save_artifact(self.filepath)
        self.mock_logger.warning.assert_not_called()

    def test_save_artifact_in_job_appends_file_to_archive(self):
        self._mock_foundations_context.is_in_running_job.return_value = True
        self._mock_foundations_context.job_id.return_value = self.job_id

        save_artifact(self.filepath)
        self._mock_archive.append_file.assert_called_once_with('artifacts', self.filepath, self.job_id, target_name=None)

    def test_save_artifact_outside_job_not_saving_artifact(self):
        self._mock_foundations_context.is_in_running_job.return_value = False
        load_archive = self.patch('foundations_contrib.archiving.load_archive')
        
        save_artifact(self.filepath)
        load_archive.assert_not_called()

    def test_save_artifact_in_job_appends_metadata_to_archive(self):
        import os.path as path

        self._mock_foundations_context.is_in_running_job.return_value = True
        self._mock_foundations_context.job_id.return_value = self.job_id

        filename = path.basename(self.filepath)
        _, extension = path.splitext(filename)
        extension_without_dot = extension[1:]

        save_artifact(self.filepath)
        self._mock_archive.append.assert_called_with(f'artifacts/{path.basename(self.filepath)}.metadata', {'file_extension': extension_without_dot}, self.job_id)

    def test_save_artifact_in_job_with_key_appends_file_to_archive_using_key_as_target(self):
        self._mock_foundations_context.is_in_running_job.return_value = True
        self._mock_foundations_context.job_id.return_value = self.job_id

        save_artifact(self.filepath, key=self.key)
        self._mock_archive.append_file.assert_called_once_with('artifacts', self.filepath, self.job_id, target_name=self.key)

    def test_save_artifact_in_job_with_key_appends_metadata_to_archive_using_key_as_filename(self):
        import os.path as path

        self._mock_foundations_context.is_in_running_job.return_value = True
        self._mock_foundations_context.job_id.return_value = self.job_id

        filename = path.basename(self.filepath)
        _, extension = path.splitext(filename)
        extension_without_dot = extension[1:]

        save_artifact(self.filepath, key=self.key)
        self._mock_archive.append.assert_called_with(f'artifacts/{self.key}.metadata', {'file_extension': extension_without_dot}, self.job_id)

    def test_save_artifact_in_job_with_key_when_key_already_exists_for_job_logs_warning(self):
        import os.path as path

        self._mock_foundations_context.is_in_running_job.return_value = True
        self._mock_foundations_context.job_id.return_value = self.job_id

        self._mock_archive.exists = ConditionalReturn()
        self._mock_archive.exists.return_when(True, f'artifacts/{self.key}', prefix=self.job_id)

        save_artifact(self.filepath, key=self.key)
        self.mock_logger.warning.assert_called_once_with(f'Artifact "{self.key}" already exists - overwriting.')