#!/bin/bash

script_location="$(pwd)/devops/build_scripts"
source "$script_location/build_common.sh"

export NEXUS_DOCKER_REGISTRY=${NEXUS_DOCKER_REGISTRY:-docker.shehanigans.net}

source "$script_location/build_all_dist.sh" && \
    rm -rf tmp/pip_wheels && \
        mkdir -p tmp/pip_wheels && \
        cp dist/* tmp/pip_wheels && \
        cp docker/gui_Dockerfile foundations_ui && \
       $script_location/helpers/parallel.py "python $script_location/gui_and_rest_apis/build_gui.py atlas" && \
        rm -rf foundations_ui/gui_Dockerfile