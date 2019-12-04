import docker
import os
import foundations

client = docker.from_env()
build_version = os.environ['docker_build_version']
nexus_registry = os.environ['NEXUS_DOCKER_REGISTRY']

from build_gui import build_and_tag_gui_image

def main(argv):
    rest_api_docker_image = 'foundations-rest-api'
    rest_api_docker_file = 'docker/rest_api_ce_Dockerfile'
    rest_api_main_file = 'run_api_server.py'
    gui_directory = 'foundations_ui'
    gui_docker_file = 'gui_ce_Dockerfile'
    gui_docker_image = 'foundations-gui'

    build_and_tag_gui_image('.', rest_api_docker_file, f'{nexus_registry}/{rest_api_docker_image}', buildargs={'main_file': rest_api_main_file})
    build_and_tag_gui_image(gui_directory, gui_docker_file, f'{nexus_registry}/{gui_docker_image}')

if __name__ == '__main__':
    import sys
    main(sys.argv)
