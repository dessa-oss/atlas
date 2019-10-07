"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 03 2019
"""

import os
import time

from unittest import skip

from foundations_spec import let, tear_down
from .docker_test_mixin import DockerTestMixin

class ContainerTestMixin(DockerTestMixin):

    repo = 'docker.shehanigans.net'

    def set_up_container(self, image_name, timeout=60, **kwargs):
        image_name = f'{self.repo}/{image_name}:{self.tag}'
        self.container = self.docker_client.containers.run(
            image_name,
            detach=True,
            remove=True,
            **kwargs)
    
        _time = 0
        while self.container.status != 'running' and _time < timeout:
            time.sleep(0.5)
            _time += 0.5
            self.container.reload()
        self.container.reload()

    @let
    def tag(self):
        return self.faker.word()

    def tear_down(self):
        self.container.stop()

    def wait_for_container_logs(self, retries=1, log_pattern=''):
        for _ in range(retries):
            self.container.reload()
            container_logs = self.container.logs().decode()
            if container_logs and log_pattern in container_logs:
                return container_logs
            time.sleep(3)
        return 'The container logs were still empty.' 