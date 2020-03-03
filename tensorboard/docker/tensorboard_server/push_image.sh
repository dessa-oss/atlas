#!/bin/bash

pip_version=`python get_version.py`
export build_version=`echo $pip_version | sed 's/+/_/g'`
export NEXUS_DOCKER_REGISTRY=${NEXUS_DOCKER_REGISTRY:-docker.shehanigans.net/atlas}

docker push $NEXUS_DOCKER_REGISTRY/tensorboard-server:$build_version \
    && docker push $NEXUS_DOCKER_REGISTRY/tensorboard-server:latest