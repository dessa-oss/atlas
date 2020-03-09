#!/bin/bash

add_path () {
    export PYTHONPATH="$1:$PYTHONPATH"
}

cwd=`pwd`
add_path "$cwd/atlas/foundations_spec/src" && \
    add_path "$cwd/atlas/foundations_events/src" && \
    add_path "$cwd/atlas/foundations_internal/src" && \
    add_path "$cwd/atlas/foundations_core_cli/src" && \
    add_path "$cwd/atlas/foundations_atlas_cli/src" && \
    add_path "$cwd/atlas/foundations_contrib/src" && \
    add_path "$cwd/atlas/foundations_sdk/src" && \
    add_path "$cwd/atlas/foundations_authentication/src" && \
    add_path "$cwd/atlas/gcp_utils/src" && \
    add_path "$cwd/atlas/aws_utils/src" && \
    add_path "$cwd/atlas/foundations_local_docker_scheduler_plugin/src" && \
    add_path "$cwd/atlas/foundations_rest_api/src" && \
    add_path "$cwd/atlas/foundations_core_rest_api_components/src" && \

source "${cwd}/devops/set_environment_for_dev.sh"
export FOUNDATIONS_HOME=${cwd}/devenv/.foundations