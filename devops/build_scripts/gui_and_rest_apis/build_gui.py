import docker
import os
import foundations
import sys

client = docker.from_env()
build_version = os.environ['docker_build_version']
nexus_registry = os.environ['NEXUS_DOCKER_REGISTRY']


def build_and_tag_gui_image(path, dockerfile, repository, buildargs=None):
    if buildargs is None:
        buildargs = {}
    build_tag = f'{repository}:{build_version}'
    latest_tag = f'{repository}:latest'
    try:
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        streamer = client.build(
            path=path,
            tag=build_tag,
            dockerfile=dockerfile,
            decode=True,
            network_mode='host',
            buildargs=buildargs
        )
        print_logs(streamer)
        
        print(f'Tagging image {build_tag} to {latest_tag}')
        image = client.tag(repository, latest_tag)
        if image == False:
            sys.exit('Unable to tag image')
        else:
            print('Successfully tagged image')
    except docker.errors.BuildError as ex:
        print_logs(ex.build_log)


def print_logs(logs):
    for line in logs:
        if 'stream' in line:
            print(line['stream'].strip())


def main(argv):
    if len(argv) != 2:
        print('expected 1 argument')
        exit(1)

    atlas_or_orbit = argv[1]

    if atlas_or_orbit == 'atlas':
        rest_api_docker_image = 'foundations-rest-api'
        rest_api_main_file = 'run_api_server.py'
        gui_directory = 'foundations_ui'
        gui_docker_file = 'gui_ce_Dockerfile'
        gui_docker_image = 'foundations-gui'
    elif atlas_or_orbit == 'orbit':
        rest_api_docker_image = 'foundations-orbit-rest-api'
        rest_api_main_file = 'run_orbit_api_server.py'
        gui_directory = 'foundations_ui_orbit'
        gui_docker_file = 'orbit_gui_Dockerfile'
        gui_docker_image = 'foundations-orbit-gui'
    else:
        print(f'invalid argument {atlas_or_orbit}; expected "atlas" or "orbit"')
        exit(1)

    build_and_tag_gui_image('.', 'docker/rest_api_Dockerfile', f'{nexus_registry}/{rest_api_docker_image}', buildargs={'main_file': rest_api_main_file})
    build_and_tag_gui_image(gui_directory, gui_docker_file, f'{nexus_registry}/{gui_docker_image}')

if __name__ == '__main__':
    main(sys.argv)