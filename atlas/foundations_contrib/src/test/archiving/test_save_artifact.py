
from foundations_spec import *

import json
from foundations_contrib.archiving.save_artifact import save_artifact

class TestSaveArtifact(Spec):

    @let
    def mock_logger(self):
        return Mock()

    @let
    def filepath(self):
        return self.faker.file_path()

    @let
    def filepath_2(self):
        return self.faker.file_path()

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def key(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        import fakeredis

        self._redis = self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeStrictRedis())

        mock_get_logger = self.patch('foundations_contrib.global_state.log_manager.get_logger', ConditionalReturn())
        mock_get_logger.return_when(self.mock_logger, 'foundations_contrib.archiving.save_artifact')

        self._mock_foundations_job = Mock()
        mock_foundations_job_function = self.patch('foundations_contrib.global_state.current_foundations_job')

        mock_foundations_job_function.return_value = self._mock_foundations_job

        self._mock_archive = Mock()
        load_archive = self.patch('foundations_contrib.archiving.load_archive', ConditionalReturn())
        load_archive.return_when(self._mock_archive, 'artifact_archive')

        self._mock_archive.exists.return_value = False

    def test_save_artifact_outside_job_logs_warning(self):
        self._mock_foundations_job.is_in_running_job.return_value = False

        save_artifact(self.filepath)
        self.mock_logger.warning.assert_called_once_with('Cannot save artifact outside of job.')

    def test_save_artifact_in_job_does_not_log_warning(self):
        self._mock_foundations_job.is_in_running_job.return_value = True

        save_artifact(self.filepath)
        self.mock_logger.warning.assert_not_called()

    def test_save_artifact_in_job_appends_file_to_archive(self):
        self._mock_foundations_job.is_in_running_job.return_value = True
        self._mock_foundations_job.job_id = self.job_id

        save_artifact(self.filepath)
        self._mock_archive.append_file.assert_called_once_with('user_artifacts', self.filepath, self.job_id, target_name=None)

    def test_save_artifact_outside_job_not_saving_artifact(self):
        self._mock_foundations_job.is_in_running_job.return_value = False
        load_archive = self.patch('foundations_contrib.archiving.load_archive')
        
        save_artifact(self.filepath)
        load_archive.assert_not_called()

    def test_save_artifact_in_job_saves_metadata_in_redis(self):
        import os.path as path

        self._mock_foundations_job.is_in_running_job.return_value = True
        self._mock_foundations_job.job_id = self.job_id

        filename = path.basename(self.filepath)
        _, extension = path.splitext(filename)
        extension_without_dot = extension[1:]

        save_artifact(self.filepath)
        
        basename = path.basename(self.filepath)

        artifact_metadata = json.loads(self._redis.get(f'jobs:{self.job_id}:user_artifact_metadata'))
        expected_metadata = {
            'key_mapping': {
                basename: basename
            },
            'metadata': {
                basename: {}
            }
        }

        self.assertEqual(expected_metadata, artifact_metadata)

    def test_save_two_artifacts_in_job_saves_metadata_for_both_in_redis(self):
        import os.path as path

        self._mock_foundations_job.is_in_running_job.return_value = True
        self._mock_foundations_job.job_id = self.job_id

        save_artifact(self.filepath)
        save_artifact(self.filepath_2)
        
        basename =  path.basename(self.filepath)
        basename_2 = path.basename(self.filepath_2)

        artifact_metadata = json.loads(self._redis.get(f'jobs:{self.job_id}:user_artifact_metadata'))
        expected_metadata = {
            'key_mapping': {
                basename: basename,
                basename_2: basename_2
            },
            'metadata': {
                basename: {},
                basename_2: {}
            }
        }

        self.assertEqual(expected_metadata, artifact_metadata)

    def test_save_two_artifacts_with_different_keys_in_job_does_not_print_warning(self):
        import os.path as path

        self._mock_foundations_job.is_in_running_job.return_value = True
        self._mock_foundations_job.job_id = self.job_id

        save_artifact(self.filepath)
        save_artifact(self.filepath_2)
        
        self.mock_logger.warning.assert_not_called()

    def test_save_artifact_in_job_with_key_appends_file_to_archive_using_basename_as_target(self):
        self._mock_foundations_job.is_in_running_job.return_value = True
        self._mock_foundations_job.job_id = self.job_id

        save_artifact(self.filepath, key=self.key)
        self._mock_archive.append_file.assert_called_once_with('user_artifacts', self.filepath, self.job_id, target_name=None)

    def test_save_artifact_in_job_with_key_appends_metadata_to_archive_using_key_as_filename(self):
        import os.path as path

        self._mock_foundations_job.is_in_running_job.return_value = True
        self._mock_foundations_job.job_id = self.job_id

        save_artifact(self.filepath, key=self.key)
        basename = path.basename(self.filepath)

        artifact_metadata = json.loads(self._redis.get(f'jobs:{self.job_id}:user_artifact_metadata'))
        expected_metadata = {
            'key_mapping': {
                self.key: basename
            },
            'metadata': {
                basename: {}
            }
        }

        self.assertEqual(expected_metadata, artifact_metadata)

    def test_save_artifact_in_job_with_key_when_key_already_exists_for_job_logs_warning(self):
        self._mock_foundations_job.is_in_running_job.return_value = True
        self._mock_foundations_job.job_id = self.job_id

        save_artifact(self.filepath, key=self.key)
        save_artifact(self.filepath_2, key=self.key)
        self.mock_logger.warning.assert_called_once_with(f'Artifact "{self.key}" already exists - overwriting.')

    def test_save_artifact_in_job_with_key_when_key_already_exists_removes_metadata_for_old_file(self):
        import os.path as path

        self._mock_foundations_job.is_in_running_job.return_value = True
        self._mock_foundations_job.job_id = self.job_id

        save_artifact(self.filepath, key=self.key)
        save_artifact(self.filepath_2, key=self.key)
        
        basename = path.basename(self.filepath_2)

        artifact_metadata = json.loads(self._redis.get(f'jobs:{self.job_id}:user_artifact_metadata'))
        expected_metadata = {
            'key_mapping': {
                self.key: basename
            },
            'metadata': {
                basename: {}
            }
        }

        self.assertEqual(expected_metadata, artifact_metadata)

    def test_save_artifact_in_job_without_key_when_artifact_already_exists_for_job_logs_warning(self):
        import os.path as path

        self._mock_foundations_job.is_in_running_job.return_value = True
        self._mock_foundations_job.job_id = self.job_id

        filename = path.basename(self.filepath)

        save_artifact(self.filepath)
        save_artifact(f'{self.filepath_2}/{self.filepath}')
        self.mock_logger.warning.assert_called_once_with(f'Artifact "{filename}" already exists - overwriting.')