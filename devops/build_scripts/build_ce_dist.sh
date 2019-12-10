#!/bin/bash

script_location="$(pwd)/devops/build_scripts"
source "$script_location/build_common.sh"

cwd=`pwd`

rm -rf dist/* && \
    build_module foundations_internal foundations_internal $cwd atlas && \
    build_module foundations_events foundations_events $cwd atlas && \
    build_module foundations_contrib foundations_contrib $cwd atlas && \
    build_module foundations_local_docker_scheduler_plugin foundations_local_docker_scheduler_plugin $cwd atlas && \
    build_module foundations_sdk dessa_foundations $cwd atlas && \
    build_module foundations_core_rest_api_components foundations_core_rest_api_components $cwd atlas && \
    build_module foundations_rest_api foundations_rest_api $cwd atlas && \
    echo "Successfully build atlas-ce wheels"