#!/bin/bash

source activate_dev_env.sh
source ./devops/set_environment_for_docker_scheduler.sh

cwd=`pwd`
F9S_ENV_TYPE=$1

if [[ $F9S_ENV_TYPE == "atlas" ]]; then
    UI_FOLDER="foundations_ui"
    FIXTURE_FOLDER="atlas_scheduler"
    $cwd/devops/startup_frontend_dev_atlas.sh
else
    UI_FOLDER="foundations_ui_orbit"
    FIXTURE_FOLDER="orbit_acceptance"
    $cwd/devops/startup_frontend_dev_orbit.sh
fi
cd $UI_FOLDER \
    && yarn install --silent \
    && export CYPRESS_LOCAL_FOUNDATIONS_HOME="${cwd}/${UI_FOLDER}/cypress/fixtures/${FIXTURE_FOLDER}/.foundations" \
    && export CYPRESS_SCHEDULER_IP=127.0.0.1 \
    && export CYPRESS_PROXY_PORT=$AUTH_PROXY_PORT \
    && export CYPRESS_SCHEDULER_FOUNDATIONS_HOME=${FOUNDATIONS_HOME} \
    && export CYPRESS_SCHEDULER_REDIS_PORT=6379 \
    && export CYPRESS_GUI_HOST=127.0.0.1\
    && export CYPRESS_GUI_PORT=3000 \
    && npm run cy:run -- --headed