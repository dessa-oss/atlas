import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.modules[__name__].__file__), "..")))


def main(argv):
    from helpers.docker_utils import build_and_tag_gui_image, nexus_registry

    if len(argv) != 2:
        print('expected 1 argument .... specify whether to build gui for orbit or atlas')
        exit(1)

    atlas_or_orbit = argv[1]
    rest_api_docker_image = ""
    rest_api_main_file = ""
    gui_directory = ""
    gui_docker_file = ""
    gui_docker_image = ""

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

    build_and_tag_gui_image(
        '.',
        'docker/rest_api_Dockerfile',
        f'{nexus_registry}/{rest_api_docker_image}',
        buildargs={'main_file': rest_api_main_file}
    )
    build_and_tag_gui_image(
        gui_directory,
        gui_docker_file,
        f'{nexus_registry}/{gui_docker_image}'
    )


if __name__ == '__main__':
    import sys
    main(sys.argv)
