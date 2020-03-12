
import os
import time

from unittest import skip

from foundations_spec import let, tear_down
from .docker_test_mixin import DockerTestMixin

class ContainerTestMixin(DockerTestMixin):

    repo = 'us.gcr.io/atlas'

    def set_up_container(self, image_name, timeout=60, **kwargs):
        self.containers = getattr(self, 'containers', {})

        container_name = kwargs.get('name', image_name)

        image_name = f'{self.repo}/{image_name}:{self.tag}'
        container = self.docker_client.containers.run(
            image_name,
            detach=True,
            remove=True,
            **kwargs)
    
        self.containers[container_name] = container

        _time = 0
        while container.status != 'running' and _time < timeout:
            time.sleep(0.5)
            _time += 0.5
            container.reload()
        container.reload()

    @let
    def tag(self):
        return self.faker.word()

    def tear_down(self):
        for container in self.containers.values():
            container.stop()

    def wait_for_container_logs(self, container_name, retries=1, log_pattern=''):
        container = self.containers[container_name]

        for _ in range(retries):
            container.reload()
            container_logs = container.logs().decode()
            if container_logs and log_pattern in container_logs:
                return container_logs
            time.sleep(3)
        return 'The container logs were still empty.' 