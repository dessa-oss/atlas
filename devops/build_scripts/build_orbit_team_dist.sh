#!/bin/bash

script_location="$(pwd)/devops/build_scripts"
source "$script_location/build_common.sh"

cwd=`pwd`

rm -rf dist/* && \
    build_module foundations_internal foundations_internal $cwd orbit && \
    build_module foundations_events foundations_events $cwd orbit && \
    build_module foundations_contrib foundations_contrib $cwd orbit && \
    build_module foundations_core_cli foundations_core_cli $cwd orbit && \
    build_module foundations_orbit_cli foundations_orbit_cli $cwd orbit && \
    build_module foundations_authentication foundations_authentication $cwd && \
    build_module foundations_local_docker_scheduler_plugin foundations_local_docker_scheduler_plugin $cwd orbit && \
    build_module foundations_sdk dessa_foundations $cwd orbit && \
    build_module foundations_orbit_sdk foundations_orbit $cwd orbit && \
    build_module foundations_core_rest_api_components foundations_core_rest_api_components $cwd orbit && \
    build_module foundations_rest_api foundations_rest_api $cwd orbit && \
    build_module foundations_orbit_rest_api foundations_orbit_rest_api $cwd orbit && \
    echo "Successfully build orbit-team wheels"