#!/bin/bash

export NEXUS_DOCKER_STAGING="844731274526.dkr.ecr.us-west-2.amazonaws.com"
export DOCKER_REGISTRY="844731274526.dkr.ecr.us-west-2.amazonaws.com"
source ./devops/set_environment_for_dev.sh
 
script_location="$(pwd)/devops/build_scripts"
cwd=`pwd`

$script_location/build_dist.sh && \

    echo "Building Atlas REST API and GUI Image" && \
    NEXUS_DOCKER_REGISTRY=$NEXUS_DOCKER_STAGING/atlas $cwd/foundations_ui/build_image.sh && \

    echo "Successfully built images" || echo "Failed to build images"

