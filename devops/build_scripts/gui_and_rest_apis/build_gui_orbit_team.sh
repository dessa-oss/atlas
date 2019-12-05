#!/bin/bash

export PACKAGE_NAME=${PACKAGE_NAME:-orbit-team-dev}

# convert the NEXUS_DOCKER_REGISTRY to the project specific domain if not converted before
if [[ $NEXUS_DOCKER_REGISTRY != *"$PACKAGE_NAME"* ]]; then
  export NEXUS_DOCKER_REGISTRY="$NEXUS_DOCKER_REGISTRY/$PACKAGE_NAME"
fi

script_location="$(pwd)/devops/build_scripts"
source "$script_location/build_common.sh"

if [ $? -eq 0 ]
then
    rm -rf tmp/pip_wheels \
        && mkdir -p tmp/pip_wheels \
        && cp dist/* tmp/pip_wheels \
        && python $script_location/gui_and_rest_apis/build_gui_orbit_team.py
fi