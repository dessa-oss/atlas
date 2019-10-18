"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 03 2019
"""

from foundations_spec import *

class DockerTestMixin(object):

    @let
    def docker_client(self):
        import docker
        return docker.from_env()

    def _create_temp_directories(self, *directory_names):
        import tempfile

        self._temp_directories = {}

        for directory_name in directory_names:
            self._temp_directories[directory_name] = tempfile.mkdtemp()

    def _cleanup_temp_directories(self):
        import shutil

        for directory_name in self._temp_directories:
            shutil.rmtree(self._temp_directories[directory_name], ignore_errors=True)
