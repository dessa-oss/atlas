# Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
# Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Susan Davis <s.davis@dessa.com>, 12 2019

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.modules[__name__].__file__), "..")))

to_be_released = os.environ.get('RELEASED', False)


def build_worker_tags_for_local_development():
    return ['orbit/worker', 'atlas-ce/worker', 'atlas-ce/worker-gpu']


def build_worker_tags_for_release():
    from helpers.docker_utils import build_version, nexus_registry

    local_worker_tags = build_worker_tags_for_local_development()
    return list(map(lambda worker: f'{nexus_registry}/{worker}:{build_version}', local_worker_tags))


def build_worker_images():
    from helpers.docker_utils import run_docker_build
    
    worker_tags = build_worker_tags_for_release() if to_be_released else build_worker_tags_for_local_development()
    worker_file_path = './docker/worker_images/'
    non_gpu_dockerfile = 'worker_Dockerfile'
    gpu_dockerfile = 'worker_tensorflow_gpu_Dockerfile'

    for worker_tag in worker_tags:
        dockerfile = gpu_dockerfile if 'gpu' in worker_tag else non_gpu_dockerfile
        print(f'Building {worker_tag} with dockerfile {dockerfile}')
        latest_tag = f"{worker_tag.split(':')[:-1][0]}:latest" if to_be_released else f"{worker_tag}:latest"
        run_docker_build(worker_file_path, dockerfile, worker_tag, latest_tag, None)


if __name__ == '__main__':
    build_worker_images()
