#!/bin/bash

cli=$1

unset FOUNDATIONS_CLI
script_location="$(pwd)/devops/build_scripts"
source "$script_location/build_common.sh"

cwd=`pwd`

rm -rf dist/* && \
    build_module foundations_spec foundations_spec $cwd && \
    build_module foundations_internal foundations_internal $cwd && \
    build_module foundations_events foundations_events $cwd && \
    build_module foundations_contrib foundations_contrib $cwd && \
    build_module foundations_cli foundations_cli $cwd && \
    build_module foundations_orbit_sdk foundations_orbit $cwd && \
    build_module gcp_utils foundations_gcp $cwd && \
    build_module ssh_utils foundations_ssh $cwd && \
    build_module aws_utils foundations_aws $cwd && \
    build_module foundations_local_docker_scheduler_plugin foundations_local_docker_scheduler_plugin $cwd && \
    build_module foundations_sdk dessa_foundations $cwd && \
    build_module foundations_core_rest_api_components foundations_core_rest_api_components $cwd && \
    build_module foundations_rest_api foundations_rest_api $cwd && \
    build_module foundations_orbit_rest_api foundations_orbit_rest_api $cwd && \

unset FOUNDATIONS_CLI
