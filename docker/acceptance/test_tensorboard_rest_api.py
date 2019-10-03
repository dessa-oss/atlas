"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file,
via any medium is strictly prohibited, proprietary and confidential.
Written by Susan Davis <s.davis@dessa.com>, 06 2018
"""

from foundations_spec import Spec, set_up, tear_down
from .mixins.container_test_mixin import ContainerTestMixin

class TestTensorboardRestAPI(Spec, ContainerTestMixin):

    @set_up
    def set_up(self):
        from foundations_contrib.utils import run_command, cd
    
        with cd('tensorboard_rest_api'):
            run_command(f'./build.sh {self.tag}')
        super().set_up_container('tensorboard-rest-api')

    @tear_down
    def tear_down(self):
        super().tear_down()

    def test_starts_tensorboard_rest_api(self):
        self.container.reload()
        container_logs = self.wait_for_container_logs(retries=5)
        self.assertIn('* Running on http://0.0.0.0:5000/', container_logs)
