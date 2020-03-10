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

export FOUNDATIONS_HOME=${cwd}/devenv/.foundations
export FOUNDATIONS_SCHEDULER_URL="http://localhost:5000"
export REDIS_URL="redis://localhost:5556"

# CYPRESS Environment Variables
UI_FOLDER="foundations_ui"
FIXTURE_FOLDER="atlas_scheduler"

export CYPRESS_LOCAL_FOUNDATIONS_HOME="${CWD}/${UI_FOLDER}/cypress/fixtures/${FIXTURE_FOLDER}/.foundations" \
export CYPRESS_SCHEDULER_IP="localhost"
export CYPRESS_SCHEDULER_FOUNDATIONS_HOME=$FOUNDATIONS_HOME 
export CYPRESS_SCHEDULER_REDIS_PORT=$REDIS_PORT 
export CYPRESS_GUI_HOST="localhost"
export CYPRESS_GUI_PORT=$GUI_PORT 