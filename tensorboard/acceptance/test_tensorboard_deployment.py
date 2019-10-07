"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Austin Mackillop, 08 2019
"""

from unittest import skip
import subprocess
from subprocess import PIPE
import requests
import yaml

from foundations_spec import *
from .tensorboard_test_base import TensorboardTestBase



@skip('Not implemented yet')
class TestTensorboardDeployment(TensorboardTestBase):

    @let
    def kubernetes_master_ip(self):
        from urllib.parse import urlparse

        config_yaml = subprocess.check_output(['kubectl', 'config', 'view'])
        config = yaml.load(config_yaml)
        current_context = config['current-context']
        cluster_name = [item for item in config['contexts']
                        if item['name'] == current_context][0]['context']['cluster']
        cluster_server = [item for item in config['clusters']
                          if item['name'] == cluster_name][0]['cluster']['server']
        return urlparse(cluster_server).hostname

    def test_can_mount_volumes_to_containers_in_pods(self):
        self.assertTrue(self._directory_exists_in_container(
            'tensorboard-rest-api', '/logs'))
        self.assertTrue(self._directory_exists_in_container(
            'tensorboard-server', '/logs'))
        self.assertTrue(self._directory_exists_in_container(
            'tensorboard-rest-api', '/archive'))
        self.assertTrue(self._directory_exists_in_container(
            'tensorboard-server', '/archive'))

    def test_tensorboard_rest_api_creates_symbolic_links_in_logdir_to_archive(self):
        test_file_content = 'hello'
        job_id = 123
        sync_dir_name = 'abc'
        sync_dir = f'/archive/archive/{job_id}/synced_directories/{sync_dir_name}'
        test_file_path = f'{sync_dir}/test.txt'
        test_link_path = f'/logs/{job_id}/{sync_dir_name}/test.txt'

        create_test_file = (
            f'kubectl exec -n {self._namespace} -it {self.pod_name} -c tensorboard-rest-api -- '
            f'sh -c "mkdir -p {sync_dir} && echo \"{test_file_content}\" > {test_file_path}"')
        self.kubernetes_api_wrapper.run_process(
            create_test_file, shell=True, check=True, stdout=PIPE)

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
                f'http://{self.kubernetes_master_ip}:32767/create_sym_links',
                json=payload_from_frontend)
        except requests.HTTPError as e:
            msg = f'HTTP Error -> {e.response.text}'
            raise AssertionError(msg)

        cat_linked_file = (f'kubectl exec -n {self._namespace} {self.pod_name} '
                           f'-c tensorboard-server -- cat {test_link_path}')
        linked_file_content = self.kubernetes_api_wrapper.run_process(
            cat_linked_file, shell=True, check=True, stdout=PIPE).stdout.decode().strip()
        self.assertEqual(test_file_content, linked_file_content)

    def _directory_exists_in_container(self, container, directory):
        command = (f'kubectl exec -n {self._namespace} -it {self.pod_name} '
                   f'-c {container} -- [ -d "{directory}" ] && echo "exists"')
        directory_exists = self.kubernetes_api_wrapper.run_process(
            command,
            shell=True,
            stdout=PIPE).stdout.decode().strip()
        return directory_exists == 'exists'


def _make_request(method: str, url: str, **kwargs) -> requests.Response:
    """Make a request. Raises an exception if unsuccessful."""
    resp = requests.request(method, url, **kwargs)
    if resp.status_code < 200 or resp.status_code >= 300:
        resp.raise_for_status()
    return resp
