import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.modules[__name__].__file__), "..")))


def main():
    from helpers.docker_utils import build_and_tag_gui_image, nexus_registry
    
    rest_api_docker_image = 'foundations-orbit-rest-api'
    rest_api_docker_file = 'docker/rest_api_orbit_team_Dockerfile'
    rest_api_main_file = 'run_orbit_api_server.py'
    gui_directory = 'foundations_ui_orbit'
    gui_docker_file = '../docker/gui_orbit_Dockerfile'
    gui_docker_image = 'foundations-orbit-gui'

    build_and_tag_gui_image('.', rest_api_docker_file, f'{nexus_registry}/{rest_api_docker_image}', buildargs={'main_file': rest_api_main_file})
    build_and_tag_gui_image(gui_directory, gui_docker_file, f'{nexus_registry}/{gui_docker_image}')


if __name__ == '__main__':
    main()
