"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file,
via any medium is strictly prohibited, proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 06 2018
"""
import re

from foundations_spec import Spec, set_up, tear_down
from .mixins.container_test_mixin import ContainerTestMixin

class TestTensorboardServer(Spec, ContainerTestMixin):

    @set_up
    def set_up(self):
        from foundations_contrib.utils import run_command, cd
        with cd('docker/tensorboard_server'):
            run_command(f'./build_image.sh {self.tag}')
        super().set_up_container('tensorboard-server')
    
    @tear_down
    def tear_down(self):
        super().tear_down()

    def test_starts_tensorboard_server(self):

        container_logs = self.wait_for_container_logs(retries=5, log_pattern='TensorBoard')
        expected_message = re.compile(
            r'TensorBoard [0-9.]+ at http:\/\/localhost:6006\/ \(Press CTRL\+C to quit\)')
        try:
            self.assertIsNotNone(expected_message.search(container_logs))
        except AssertionError:
            msg = '\n'.join(
                [f'Expected regex {expected_message.pattern} was not found in the container logs.',
                 'Container logs:', container_logs])
            self.fail(msg)
