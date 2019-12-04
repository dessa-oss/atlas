import docker 
import os


build_version = os.environ['docker_build_version']
nexus_password = os.environ['NEXUS_PASSWORD']
nexus_username = os.environ['NEXUS_USER']
nexus_registry = os.environ.get('NEXUS_DOCKER_REGISTRY', 'docker.shehanigans.net')

client = docker.from_env()
client.login(username=nexus_username, password=nexus_password, registry=nexus_registry)


# TODO Pull from single source (repeated for now to experiment with functionality)


def build_worker_tags_for_local_development():
    return ['orbit/worker', 'atlas-ce/worker', 'atlas-ce/worker-gpu']


def build_worker_tags_for_release():
    local_worker_tags = build_worker_tags_for_local_development()
    return list(map(lambda worker: f'{nexus_registry}/{worker}:{build_version}', local_worker_tags))


def push_image_with_tag(image_name, tag):
    full_image_name=f'{nexus_registry}/{image_name}'
    push_logs = client.images.push(repository=full_image_name, tag=tag, stream=True, decode=True)

    for log_line in push_logs:
        print(log_line)
        if 'error' in log_line:
            raise RuntimeError(log_line)


def push_image_to_repository(image_name):
    push_image_with_tag(image_name, tag=build_version)
    push_image_with_tag(image_name, tag='latest')


if __name__ == '__main__':
    workers = build_worker_tags_for_local_development()
    for worker in workers:
        push_image_to_repository(worker)