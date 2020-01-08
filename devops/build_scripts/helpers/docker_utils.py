"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 12 2019
"""
import os

build_version = os.environ['docker_build_version']
nexus_registry = os.environ.get('NEXUS_DOCKER_REGISTRY', 'docker.shehanigans.net')


def print_logs(logs, is_generator=True):
    if is_generator:
        for line in logs:
            print(line)
            if 'error' in line:
                raise RuntimeError(line)
    else:
        print(logs)

def get_docker_low_level_client():
    import docker

    nexus_password = os.environ['NEXUS_PASSWORD']
    nexus_username = os.environ['NEXUS_USER']
    return docker.APIClient(base_url='unix://var/run/docker.sock')

def run_docker_build(path, dockerfile, build_tag, latest_tag, buildargs):
    import docker
    import sys
    try:
        api_client = docker.APIClient(base_url='unix://var/run/docker.sock')
        streamer = api_client.build(
            path=path,
            tag=build_tag,
            dockerfile=dockerfile,
            decode=True,
            network_mode='host',
            buildargs=buildargs
        )
        print_logs(streamer)

        print(f'Tagging image {build_tag} to {latest_tag}')
        image = api_client.tag(build_tag, latest_tag)
        if not image:
            sys.exit('Unable to tag image')
        else:
            print('Successfully tagged image')
    except docker.errors.BuildError as ex:
        print_logs(ex.build_log)
        raise


def build_and_tag_gui_image(path, dockerfile, repository, buildargs=None):
    buildargs = {} if buildargs is None else buildargs
    build_tag = f'{repository}:{build_version}'
    latest_tag = f'{repository}:latest'
    run_docker_build(path, dockerfile, build_tag, latest_tag, buildargs)


def get_authenticated_docker_py_client():
    import docker
    nexus_password = os.environ['NEXUS_PASSWORD']
    nexus_username = os.environ['NEXUS_USER']

    client = docker.from_env()
    client.login(username=nexus_username, password=nexus_password, registry=nexus_registry)
    return client

def push_image_with_tag(image_name, tag):
    client = get_authenticated_docker_py_client()

    full_image_name=f'{nexus_registry}/{image_name}'
    push_logs = client.images.push(repository=full_image_name, tag=tag, stream=True, decode=True)

    for log_line in push_logs:
        print(log_line)
        if 'error' in log_line:
            raise RuntimeError(log_line)


def push_image_to_repository(image_name):
    push_image_with_tag(image_name, tag=build_version)
    push_image_with_tag(image_name, tag='latest')
