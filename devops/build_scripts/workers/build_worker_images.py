import docker
import os
import sys

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


def build_worker_images():
    worker_tags = build_worker_tags_for_release() if to_be_released else build_worker_tags_for_local_development()
    client = docker.from_env()
    worker_file_path = './docker/worker_images/'
    non_gpu_dockerfile = 'worker_Dockerfile'
    gpu_dockerfile = 'worker_tensorflow_gpu_Dockerfile'

    for worker_tag in worker_tags:
        dockerfile = gpu_dockerfile if 'gpu' in worker_tag else non_gpu_dockerfile
        print(f'Building {worker_tag} with dockerfile {dockerfile}')
        if to_be_released:
            latest_tag=f"{worker_tag.split(':')[:-1][0]}:latest"
        else:
            latest_tag=f"{worker_tag}:latest"
        
        try:
            client = docker.APIClient(base_url='unix://var/run/docker.sock')
            streamer = client.build(path=worker_file_path, 
                                    tag=worker_tag, 
                                    dockerfile=dockerfile, 
                                    decode=True,
                                    buildargs=None)
            print_logs(streamer)

            print(f'Tagging image {worker_tag} to {latest_tag}')
            image = client.tag(worker_tag, latest_tag)
            if image == False:
                sys.exit('Unable to tag image')
            else:
                print('Successfully tagged image')
        except docker.errors.BuildError as ex:
            print_logs(ex.build_log)

        # image, image_logs = client.images.build(path=worker_file_path, dockerfile=dockerfile, tag=worker_tag, buildargs=None)
        # image.tag(worker_tag, tag='latest')
        # print_logs(image_logs)


if __name__ == '__main__':
    build_worker_images()