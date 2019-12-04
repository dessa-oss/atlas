import docker 
import os


build_version = os.environ['docker_build_version']
nexus_password = os.environ['NEXUS_PASSWORD']
nexus_username = os.environ['NEXUS_USER']
nexus_registry = os.environ['NEXUS_DOCKER_REGISTRY']

client = docker.from_env()
client.login(username=nexus_username, password=nexus_password, registry=nexus_registry)


def push_image_with_tag(image_name, tag):
    push_logs = client.images.push(repository=nexus_registry + '/' + image_name, tag=tag, stream=True, decode=True)

    for log_line in push_logs:
        print(log_line)
        if 'error' in log_line:
            raise RuntimeError(log_line)


def push_image_to_repository(image_name):
    push_image_with_tag(image_name, tag=build_version)
    push_image_with_tag(image_name, tag='latest')


if __name__ == '__main__':
    push_image_to_repository(image_name='foundations-orbit-rest-api')
    push_image_to_repository(image_name='foundations-rest-api')
    push_image_to_repository(image_name='foundations-gui')
    push_image_to_repository(image_name='foundations-orbit-gui')