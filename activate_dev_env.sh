#!/bin/bash

add_path () {
    export PYTHONPATH="$1:$PYTHONPATH"
}

cwd=`pwd`
add_path "$cwd/foundations_spec/src" && \
    add_path "$cwd/foundations_events/src" && \
    add_path "$cwd/foundations_internal/src" && \
    add_path "$cwd/foundations_contrib/src" && \
    add_path "$cwd/foundations_sdk/src" && \
    add_path "$cwd/ssh_utils/src" && \
    add_path "$cwd/gcp_utils/src" && \
    add_path "$cwd/aws_utils/src" && \
    add_path "$cwd/foundations_local_docker_scheduler_plugin/src" && \
    add_path "$cwd/foundations_rest_api/src" && \
    add_path "$cwd/foundations_core_rest_api_components/src" && \
    add_path "$cwd/foundations_orbit_rest_api/src" && \
    add_path "$cwd/foundations_orbit_sdk/src"

export CYPRESS_GUI_HOST=localhost
export CYPRESS_SCHEDULER_IP=localhost
export CYPRESS_GUI_PORT=3000
export CYPRESS_SCHEDULER_REDIS_PORT=6379
export CYPRESS_LOCAL_FOUNDATIONS_HOME=$FOUNDATIONS_HOME
export CYPRESS_SCHEDULER_FOUNDATIONS_HOME=$FOUNDATIONS_HOME