#!/bin/bash

pip_version=`python get_version.py`
export build_version=`echo $pip_version | sed 's/+/_/g'`
export NEXUS_DOCKER_REGISTRY=${NEXUS_DOCKER_REGISTRY:-docker.shehanigans.net/atlas}

docker build --network=host -t $NEXUS_DOCKER_REGISTRY/archive_server:$build_version . \
    && docker tag $NEXUS_DOCKER_REGISTRY/archive_server:$build_version $NEXUS_DOCKER_REGISTRY/archive_server:latest