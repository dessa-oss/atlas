#!/bin/bash

script_location="$(pwd)/devops/build_scripts"
source "$script_location/build_common.sh"

rm -rf tmp/pip_wheels && \
    mkdir -p tmp/pip_wheels && \
    cp dist/* tmp/pip_wheels && \
    cp docker/gui_ce_Dockerfile foundations_ui && \
    python $script_location/gui_and_rest_apis/build_gui_ce.py && \
    rm -rf foundations_ui/gui_ce_Dockerfile
