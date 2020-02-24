
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
