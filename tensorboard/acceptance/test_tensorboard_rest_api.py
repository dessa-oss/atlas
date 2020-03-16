
import requests
from subprocess import PIPE

from foundations_spec import Spec, set_up, tear_down
from foundations_contrib.utils import run_command, cd
from .mixins.container_test_mixin import ContainerTestMixin

class TestTensorboardRestAPI(Spec, ContainerTestMixin):

    API_CONTAINER_NAME = 'tensorboard-rest-api'
    API_IMAGE_NAME = 'tensorboard-rest-api'

    SERVER_CONTAINER_NAME = 'tensorboard-server'
    SERVER_IMAGE_NAME = 'tensorboard-server'

    @set_up
    def set_up(self):
        self._create_temp_directories('archive', 'logs')

        volumes_binds = {
            self._temp_directories['archive']: {
                'bind': '/archive',
                'mode': 'rw'
            },
            self._temp_directories['logs']: {
                'bind': '/logs',
                'mode': 'rw'
            }
        }

        with cd('docker/tensorboard_rest_api'):
            run_command(f'tensorboard/docker/tensorboard_rest_api/build_image.sh {self.repo} {self.tag}', cwd='../../..')
        super().set_up_container(self.API_IMAGE_NAME, name=self.API_CONTAINER_NAME, ports={5000: 5000}, volumes=volumes_binds)

        with cd('docker/tensorboard_server'):
            run_command(f'tensorboard/docker/tensorboard/build_image.sh {self.repo} {self.tag}', cwd='../../..')
        super().set_up_container(self.SERVER_IMAGE_NAME, name=self.SERVER_CONTAINER_NAME, ports={6006: 5959}, volumes=volumes_binds)

    @tear_down
    def tear_down(self):
        super().tear_down()
        self._cleanup_temp_directories()

    def test_starts_tensorboard_rest_api(self):
        self.containers[self.API_CONTAINER_NAME].reload()
        container_logs = self.wait_for_container_logs(self.API_CONTAINER_NAME, retries=5)
        self.assertIn('* Running on http://0.0.0.0:5000/', container_logs)

    def test_tensorboard_rest_api_creates_symbolic_links_in_logdir_to_archive(self):
        test_file_content = 'hello'
        job_id = 123
        sync_dir_name = '__tensorboard__'
        sync_dir = f'/archive/archive/{job_id}/synced_directories/{sync_dir_name}'
        test_file_path = f'{sync_dir}/test.txt'
        test_link_path = f'/logs/{job_id}/test.txt'

        create_test_file = (
            f'docker exec -it {self.API_CONTAINER_NAME} '
            f'sh -c "mkdir -p {sync_dir} && echo \"{test_file_content}\" > {test_file_path}"')

        run_command(create_test_file)

        payload_from_frontend = {
            'tensorboard_locations': [
                {
                    'job_id': f'{job_id}',
                    'synced_directory': f'archive/{job_id}/synced_directories/__tensorboard__'
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

        cat_linked_file = (f'docker exec {self.SERVER_CONTAINER_NAME} '
                           f'cat {test_link_path}')
        linked_file_content = run_command(cat_linked_file).stdout.decode().strip()

        self.assertEqual(test_file_content, linked_file_content)


def _make_request(method: str, url: str, **kwargs) -> requests.Response:
    """Make a request. Raises an exception if unsuccessful."""
    resp = requests.request(method, url, **kwargs)
    if resp.status_code < 200 or resp.status_code >= 300:
        resp.raise_for_status()
    return resp
