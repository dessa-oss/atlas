"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file,
via any medium is strictly prohibited, proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 06 2018
"""
import re

from foundations_spec import Spec, set_up, tear_down
from foundations_contrib.utils import run_command, cd
from .mixins.container_test_mixin import ContainerTestMixin


class TestTensorboardServer(Spec, ContainerTestMixin):

    @set_up
    def set_up(self):
        with cd('docker/tensorboard_server'):
            run_command(f'./build_image.sh {self.repo} {self.tag}')
        super().set_up_container('tensorboard-server')

    @tear_down
    def tear_down(self):
        super().tear_down()

    def test_starts_tensorboard_server(self):
        container_logs = self.wait_for_container_logs(
            'tensorboard-server', retries=5, log_pattern='TensorBoard')
        expected_message = re.compile(
            r'TensorBoard [0-9.]+ at http:\/\/[0-9a-f]{12}:6006\/ \(Press CTRL\+C to quit\)')
        try:
            self.assertIsNotNone(expected_message.search(container_logs))
        except AssertionError:
            msg = '\n'.join(
                [f'Expected regex {expected_message.pattern} was not found in the container logs.',
                 'Container logs:', container_logs])
            self.fail(msg)
    
    # def test_tensorboard_rest_api_creates_symbolic_links_in_logdir_to_archive(self):
    #     test_file_content = 'hello'
    #     job_id = 123
    #     sync_dir_name = 'abc'
    #     sync_dir = f'/archive/archive/{job_id}/synced_directories/{sync_dir_name}'
    #     test_file_path = f'{sync_dir}/test.txt'
    #     test_link_path = f'/logs/{job_id}/{sync_dir_name}/test.txt'

    #     create_test_file = (
    #         f'kubectl exec -n {self._namespace} -it {self.pod_name} -c tensorboard-rest-api -- '
    #         f'sh -c "mkdir -p {sync_dir} && echo \"{test_file_content}\" > {test_file_path}"')
    #     self.kubernetes_api_wrapper.run_process(
    #         create_test_file, shell=True, check=True, stdout=PIPE)

    #     payload_from_frontend = {
    #         'tensorboard_locations': [
    #             {
    #                 'job_id': f'{job_id}',
    #                 'synced_directory': f'{sync_dir_name}'
    #             }
    #         ]
    #     }
    #     try:
    #         _make_request(
    #             'POST',
    #             f'http://{self.kubernetes_master_ip}:32767/create_sym_links',
    #             json=payload_from_frontend)
    #     except requests.HTTPError as e:
    #         msg = f'HTTP Error -> {e.response.text}'
    #         raise AssertionError(msg)

    #     cat_linked_file = (f'kubectl exec -n {self._namespace} {self.pod_name} '
    #                        f'-c tensorboard-server -- cat {test_link_path}')
    #     linked_file_content = self.kubernetes_api_wrapper.run_process(
    #         cat_linked_file, shell=True, check=True, stdout=PIPE).stdout.decode().strip()
    #     self.assertEqual(test_file_content, linked_file_content)