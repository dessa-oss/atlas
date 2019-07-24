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

    @set_up
    def set_up(self):
        mock_get_logger = self.patch('foundations_contrib.global_state.log_manager.get_logger', ConditionalReturn())
        mock_get_logger.return_when(self.mock_logger, 'foundations_contrib.archiving.save_artifact')

        self._mock_foundations_context = Mock()
        mock_foundations_context_function = self.patch('foundations_contrib.global_state.current_foundations_context')

        mock_foundations_context_function.return_value = self._mock_foundations_context

    def test_save_artifact_outside_job_logs_warning(self):
        self._mock_foundations_context.is_in_running_job.return_value = False

        save_artifact(self.faker.file_path())
        self.mock_logger.warning.assert_called_once_with('Cannot save artifact outside of job.')

    def test_save_artifact_in_job_does_not_log_warning(self):
        self._mock_foundations_context.is_in_running_job.return_value = True

        save_artifact(self.faker.file_path())
        self.mock_logger.warning.assert_not_called()