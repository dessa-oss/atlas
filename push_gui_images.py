import docker 
import os

client = docker.from_env()
build_version = os.environ['build_version']
nexus_password = os.environ['NEXUS_PASSWORD']
nexus_username = os.environ['NEXUS_USER']
nexus_registry = os.environ['NEXUS_DOCKER_REGISTRY']

def push_image_with_tag(image_name, tag):
    try:
        push_logs = client.images.push(repository=nexus_registry + '/' + image_name, tag=tag)
    finally:
        print(push_logs)

def push_image_to_repository(image_name):
    push_image_with_tag(image_name, tag=build_version)
    push_image_with_tag(image_name, tag='latest')

client.login(username=nexus_username, password=nexus_password, registry=nexus_registry)

push_image_to_repository(image_name='foundations-rest-api')
push_image_to_repository(image_name='foundations-gui')

