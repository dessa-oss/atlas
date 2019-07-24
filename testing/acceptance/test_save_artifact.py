"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations import save_artifact

class TestSaveArtifact(Spec):

    @let
    def local_file_directory(self):
        from uuid import uuid4
        return str(uuid4())

    @let
    def artifact_file_path(self):
        import os.path as path

        return path.join(self.local_file_directory, 'cool-artifact.txt')

    @let
    def artifact_file_contents(self):
        return self.faker.sentence()

    @set_up
    def set_up(self):
        import os

        os.mkdir(self.local_file_directory)
        with open(self.artifact_file_path, 'w') as artifact_file:
            artifact_file.write(self.artifact_file_contents)

    @tear_down
    def tear_down(self):
        import shutil
        shutil.rmtree(self.local_file_directory)

    def test_save_artifact_outside_of_job_logs_warning(self):
        import subprocess

        completed_process = subprocess.run(['bash', '-c', 'cd acceptance/fixtures/save_artifact_outside_of_job && python main.py'], stdout=subprocess.PIPE)
        process_output = completed_process.stdout.decode()
        self.assertIn('WARNING', process_output)
        self.assertIn('Cannot save artifact outside of job.', process_output)