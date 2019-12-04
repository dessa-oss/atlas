import docker
import os

build_version = os.environ['docker_build_version']
to_be_released = os.environ.get('RELEASED', False)


def print_logs(logs):
    for line in logs:
        if 'stream' in line:
            print(line['stream'].strip())


def build_worker_tags_for_local_development():
    return ['orbit/worker', 'atlas-ce/worker', 'atlas-ce/worker-gpu']


def build_worker_tags_for_release():
    nexus_registry = os.environ['NEXUS_DOCKER_REGISTRY']
    local_worker_tags = build_worker_tags_for_local_development()
    return list(map(lambda worker: f'{nexus_registry}/{worker}:{build_version}', local_worker_tags))


worker_tags = build_worker_tags_for_release() if to_be_released else build_worker_tags_for_local_development()
client = docker.from_env()
worker_file_path = './docker/worker_images/'
non_gpu_dockerfile = 'worker_Dockerfile'
gpu_dockerfile = 'worker_tensorflow_gpu_Dockerfile'

for worker_tag in worker_tags:
    dockerfile = gpu_dockerfile if 'gpu' in worker_tag else non_gpu_dockerfile
    print(f'Building {worker_tag} with dockerfile {dockerfile}')
    image, image_logs = client.images.build(path=worker_file_path, dockerfile=dockerfile, tag=worker_tag, buildargs=None)
    image.tag(worker_tag, tag='latest')
    print_logs(image_logs)
