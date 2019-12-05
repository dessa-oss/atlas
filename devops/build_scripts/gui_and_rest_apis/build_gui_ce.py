# Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
# Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Susan Davis <s.davis@dessa.com>, 12 2019

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.modules[__name__].__file__), "..")))


def main():
    from helpers.docker_utils import build_and_tag_gui_image, nexus_registry
    
    rest_api_docker_image = 'foundations-rest-api'
    rest_api_docker_file = 'docker/rest_api_ce_Dockerfile'
    rest_api_main_file = 'run_api_server.py'
    gui_directory = 'foundations_ui'
    gui_docker_file = 'gui_ce_Dockerfile'
    gui_docker_image = 'foundations-gui'

    build_and_tag_gui_image('.', rest_api_docker_file, f'{nexus_registry}/{rest_api_docker_image}', buildargs={'main_file': rest_api_main_file})
    build_and_tag_gui_image(gui_directory, gui_docker_file, f'{nexus_registry}/{gui_docker_image}')


if __name__ == '__main__':
    main()
