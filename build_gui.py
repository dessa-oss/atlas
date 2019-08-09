import docker
import os
import foundations

client = docker.from_env()
build_version = os.environ['build_version']
nexus_registry = os.environ['NEXUS_DOCKER_REGISTRY']

def build_and_tag_gui_image(path, dockerfile, repository, buildargs=None):
    if buildargs is None:
        buildargs = {}

    try:
        image, image_logs = client.images.build(path=path, dockerfile=dockerfile, tag='{}:{}'.format(repository, build_version), buildargs=buildargs)
        image.tag(repository, tag='latest')
    finally:
        for line in image_logs:
            print(line)

build_and_tag_gui_image('.', 'docker/rest_api_Dockerfile', '{}/foundations-rest-api'.format(nexus_registry), buildargs={'main_file': 'run_api_server.py'})
build_and_tag_gui_image('.', 'docker/rest_api_Dockerfile', '{}/foundations-orbit-rest-api'.format(nexus_registry), buildargs={'main_file': 'run_orbit_api_server.py'})
build_and_tag_gui_image('foundations_ui', 'gui_Dockerfile', '{}/foundations-gui'.format(nexus_registry))