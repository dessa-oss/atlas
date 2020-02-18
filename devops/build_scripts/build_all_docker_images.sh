#!/bin/bash

export NEXUS_DOCKER_STAGING=docker-staging.shehanigans.net
source ./devops/set_environment_for_docker_scheduler.sh
 
script_location="$(pwd)/devops/build_scripts"
$script_location/build_all_dist.sh && \

    echo "Building Atlas REST API and GUI Image" && \
    NEXUS_DOCKER_REGISTRY=$NEXUS_DOCKER_STAGING/atlas-ce $script_location/gui_and_rest_apis/build_gui_ce.sh && \
    
    echo "Building Orbit REST API and GUI Image" && \
    NEXUS_DOCKER_REGISTRY=$NEXUS_DOCKER_STAGING PACKAGE_NAME=orbit-team $script_location/gui_and_rest_apis/build_gui_orbit_team.sh && \

    echo "Successfully built images" || echo "Failed to build images"

