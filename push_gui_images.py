import docker 
import os


build_version = os.environ['build_version']
nexus_password = os.environ['NEXUS_PASSWORD']
nexus_username = os.environ['NEXUS_USER']
nexus_registry = os.environ['NEXUS_DOCKER_REGISTRY']

client = docker.from_env()
client.login(username=nexus_username, password=nexus_password, registry=nexus_registry)


def push_image_with_tag(image_name, tag):
    import json

    push_logs = client.images.push(repository=nexus_registry + '/' + image_name, tag=tag, stream=True)

    for log_line in push_logs:
        log_line = log_line.rstrip()
        log_object = json.loads(log_line)
        print(log_object)

        if 'error' in log_object:
            raise RuntimeError(log_object)


def push_image_to_repository(image_name):
    push_image_with_tag(image_name, tag=build_version)
    push_image_with_tag(image_name, tag='latest')


if __name__ == '__main__':
    push_image_to_repository(image_name='foundations-orbit-rest-api')
    push_image_to_repository(image_name='foundations-rest-api')
    push_image_to_repository(image_name='foundations-gui')
    push_image_to_repository(image_name='foundations-orbit-gui')