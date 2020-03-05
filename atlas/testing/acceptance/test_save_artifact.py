
from foundations_spec import *

import json
import foundations

from foundations_contrib.global_state import config_manager
from acceptance.mixins.run_local_job import RunLocalJob

class TestSaveArtifact(Spec, RunLocalJob):

    @let
    def _artifact_archive(self):
        from foundations_contrib.archiving import load_archive
        return load_archive('artifact_archive')

    @let
    def _redis_connection(self):
        from foundations_contrib.global_state import redis_connection
        return redis_connection

    def test_save_artifact_outside_of_job_logs_warning(self):
        from foundations_spec.extensions import run_process
        
        process_output = run_process(['python', 'main.py'], 'acceptance/fixtures/save_artifact')
        self.assertIn('WARNING', process_output)
        self.assertIn('Cannot save artifact outside of job.', process_output)

    def test_save_artifact_with_filepath_only_saves_file_with_key_equal_to_basename_and_saves_metadata_with_extension_in_redis(self):
        self._deploy_job_file('acceptance/fixtures/save_artifact')
        artifact_contents = self._artifact_archive.fetch_binary('user_artifacts/cool-artifact.txt', self.job_id)
        artifact_metadata = json.loads(self._redis_connection.get(f'jobs:{self.job_id}:user_artifact_metadata'))

        expected_metadata = {
            'key_mapping': {
                'cool-artifact.txt': 'cool-artifact.txt'
            },
            'metadata': {
                'cool-artifact.txt': {}
            }
        }

        self.assertEqual(b'contents of artifact', artifact_contents)
        self.assertEqual(expected_metadata, artifact_metadata)

    def test_save_artifact_with_filepath_and_key_saves_file_with_specified_key_and_saves_metadata_with_extension_in_redis(self):
        self._deploy_job_file('acceptance/fixtures/save_artifact_with_key')
        artifact_contents = self._artifact_archive.fetch_binary('user_artifacts/cool-artifact.txt', self.job_id)
        artifact_metadata = json.loads(self._redis_connection.get(f'jobs:{self.job_id}:user_artifact_metadata'))

        expected_metadata = {
            'key_mapping': {
                'this-key': 'cool-artifact.txt'
            },
            'metadata': {
                'cool-artifact.txt': {}
            }
        }

        self.assertEqual(b'contents of artifact', artifact_contents)
        self.assertEqual(expected_metadata, artifact_metadata)

    def test_save_artifact_twice_with_filepath_and_key_saves_file_with_specified_key_and_saves_metadata_with_extension_in_redis(self):
        self._deploy_job_file('acceptance/fixtures/save_artifact_with_key_twice')
        artifact_contents = self._artifact_archive.fetch_binary('user_artifacts/cooler-artifact.other', self.job_id)
        artifact_metadata = json.loads(self._redis_connection.get(f'jobs:{self.job_id}:user_artifact_metadata'))

        expected_metadata = {
            'key_mapping': {
                'this-key': 'cooler-artifact.other'
            },
            'metadata': {
                'cooler-artifact.other': {}
            }
        }

        self.assertEqual(b'contents of cooler artifact', artifact_contents)
        self.assertEqual(expected_metadata, artifact_metadata)

    def test_save_artifact_twice_with_filepath_and_key_logs_appropriate_warning(self):
        process_output = self._deploy_job_file('acceptance/fixtures/save_artifact_with_key_twice')
        self.assertIn('WARNING', process_output)
        self.assertIn('Artifact "this-key" already exists - overwriting.', process_output)

    def test_save_artifact_twice_with_filepath_only_saves_file_and_saves_metadata_with_extension_in_redis(self):
        self._deploy_job_file('acceptance/fixtures/save_artifact_twice')
        artifact_contents = self._artifact_archive.fetch_binary('user_artifacts/cool-artifact.txt', self.job_id)
        artifact_metadata = json.loads(self._redis_connection.get(f'jobs:{self.job_id}:user_artifact_metadata'))

        expected_metadata = {
            'key_mapping': {
                'cool-artifact.txt': 'cool-artifact.txt'
            },
            'metadata': {
                'cool-artifact.txt': {}
            }
        }

        self.assertEqual(b'contents of cooler artifact', artifact_contents)
        self.assertEqual(expected_metadata, artifact_metadata)

    def test_save_two_artifacts_with_different_keys_saves_files_in_archive_and_saves_metadata_with_extension_in_redis(self):
        self._deploy_job_file('acceptance/fixtures/save_artifact_with_two_different_keys')
        artifact_contents_0 = self._artifact_archive.fetch_binary('user_artifacts/cool-artifact.txt', self.job_id)
        artifact_contents_1 = self._artifact_archive.fetch_binary('user_artifacts/cooler-artifact.other', self.job_id)
        artifact_metadata = json.loads(self._redis_connection.get(f'jobs:{self.job_id}:user_artifact_metadata'))

        expected_metadata = {
            'key_mapping': {
                'this-key': 'cool-artifact.txt',
                'that-key': 'cooler-artifact.other'
            },
            'metadata': {
                'cool-artifact.txt': {},
                'cooler-artifact.other': {}
            }
        }

        self.assertEqual(b'contents of artifact', artifact_contents_0)
        self.assertEqual(b'contents of cooler artifact', artifact_contents_1)
        self.assertEqual(expected_metadata, artifact_metadata)

    def test_save_artifact_twice_with_filepath_only_logs_appropriate_warning(self):
        process_output = self._deploy_job_file('acceptance/fixtures/save_artifact_twice')
        self.assertIn('WARNING', process_output)
        self.assertIn('Artifact "cool-artifact.txt" already exists - overwriting.', process_output)