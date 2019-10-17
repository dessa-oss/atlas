"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file,
via any medium is strictly prohibited, proprietary and confidential.
Written by Susan Davis <s.davis@dessa.com>, 06 2018
"""

import requests
from subprocess import PIPE

from foundations_spec import Spec, set_up, tear_down
from foundations_contrib.utils import run_command, cd
from .mixins.container_test_mixin import ContainerTestMixin

class TestTensorboardRestAPI(Spec, ContainerTestMixin):

    CONTAINER_NAME = 'tensorboard-rest-api'
    IMAGE_NAME = 'tensorboard-rest-api'

    @set_up
    def set_up(self):
        with cd('docker/tensorboard_rest_api'):
            run_command(f'./build_image.sh {self.repo} {self.tag}')
        super().set_up_container(self.IMAGE_NAME, name=self.CONTAINER_NAME, ports={5000: 5000})

    @tear_down
    def tear_down(self):
        super().tear_down()

    def test_starts_tensorboard_rest_api(self):
        self.container.reload()
        container_logs = self.wait_for_container_logs(retries=5)
        self.assertIn('* Running on http://0.0.0.0:5000/', container_logs)

    def test_tensorboard_rest_api_creates_symbolic_links_in_logdir_to_archive(self):
        test_file_content = 'hello'
        job_id = 123
        sync_dir_name = 'abc'
        sync_dir = f'/archive/archive/{job_id}/synced_directories/{sync_dir_name}'
        test_file_path = f'{sync_dir}/test.txt'
        test_link_path = f'/logs/{job_id}/{sync_dir_name}/test.txt'

        create_test_file = (
            f'docker exec -it {self.CONTAINER_NAME} '
            f'sh -c "mkdir -p {sync_dir} && echo \"{test_file_content}\" > {test_file_path}"')

        run_command(create_test_file)

        payload_from_frontend = {
            'tensorboard_locations': [
                {
                    'job_id': f'{job_id}',
                    'synced_directory': f'{sync_dir_name}'
                }
            ]
        }
        try:
            _make_request(
                'POST',
                f'http://localhost:5000/create_sym_links',
                json=payload_from_frontend)
        except requests.HTTPError as e:
            msg = f'HTTP Error -> {e.response.text}'
            raise AssertionError(msg)

        cat_linked_file = (f'docker exec {self.CONTAINER_NAME} '
                           f'-c tensorboard-server -- cat {test_link_path}')
        linked_file_content = run_command(cat_linked_file).stdout.decode().strip()

        self.assertEqual(test_file_content, linked_file_content)


def _make_request(method: str, url: str, **kwargs) -> requests.Response:
    """Make a request. Raises an exception if unsuccessful."""
    resp = requests.request(method, url, **kwargs)
    if resp.status_code < 200 or resp.status_code >= 300:
        resp.raise_for_status()
    return resp
