"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

import foundations

class TestSaveArtifact(Spec):

    @set_up
    def set_up(self):
        import os
        import os.path as path
        import shutil

        from foundations_contrib.archiving import load_archive

        self._config_dir = path.expanduser('~/.foundations/config')
        os.makedirs(self._config_dir, exist_ok=True)
        shutil.copyfile('config/local.config.yaml', path.join(self._config_dir, 'local.config.yaml'))

        self._artifact_archive = load_archive('artifact_archive')

    @tear_down
    def tear_down(self):
        import os
        import os.path as path
        
        os.remove(path.join(self._config_dir, 'local.config.yaml'))

    def test_save_artifact_outside_of_job_logs_warning(self):
        import subprocess

        completed_process = subprocess.run(['bash', '-c', 'cd acceptance/fixtures/save_artifact && python main.py'], stdout=subprocess.PIPE)
        process_output = completed_process.stdout.decode()
        self.assertIn('WARNING', process_output)
        self.assertIn('Cannot save artifact outside of job.', process_output)

    @skip('not implemented')
    def test_save_artifact_with_filepath_only_saves_file_with_key_equal_to_basename_and_saves_metadata_file_that_contains_extension(self):
        job_deployment = foundations.deploy(job_directory='acceptance/fixtures/save_artifact')
        job_deployment.wait_for_deployment_to_complete()
        
        job_id = job_deployment.job_name()
        artifact_contents = self._artifact_archive.fetch_binary('artifacts/cool-artifact.txt', job_id)
        artifact_metadata = self._artifact_archive.fetch('artifacts/cool-artifact.txt.metadata', job_id)
        
        self.assertEqual(b'contents of artifact', artifact_contents)
        self.assertEqual({'file_extension': 'txt'}, artifact_metadata)