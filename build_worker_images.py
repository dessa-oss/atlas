import docker
import os
import foundations


build_version = os.environ['build_version']
to_be_released = os.environ.get('RELEASED', False)

def print_logs(logs):
    for line in logs:
        if 'stream' in line:
            print(line['stream'].strip())


def build_worker_tags_for_local_development():
    return ['orbit/worker', 'atlas-ce/worker']


def build_worker_tags_for_release():
    nexus_registry = os.environ['NEXUS_DOCKER_REGISTRY']
    return [f'{nexus_registry}/orbit/worker:{build_version}', f'{nexus_registry}/atlas-ce/worker:{build_version}']


worker_tags = build_worker_tags_for_release() if to_be_released else build_worker_tags_for_local_development()
client = docker.from_env()
worker_file_path='./docker/worker_images/'
dockerfile = 'worker_Dockerfile' 

for worker_tag in worker_tags:
    print(worker_tag)
    image, image_logs = client.images.build(path=worker_file_path, dockerfile=dockerfile, tag=worker_tag, buildargs=None)
    image.tag(worker_tag, tag='latest')
    print_logs(image_logs)
