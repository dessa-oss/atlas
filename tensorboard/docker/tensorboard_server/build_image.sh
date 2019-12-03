#!/bin/bash

pip_version=`python get_version.py`
export build_version=`echo $pip_version | sed 's/+/_/g'`
export NEXUS_DOCKER_REGISTRY=${NEXUS_DOCKER_REGISTRY:-docker.shehanigans.net}

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker build -t $NEXUS_DOCKER_REGISTRY/atlas-ce/tensorboard-server:$build_version $DIR
docker tag $NEXUS_DOCKER_REGISTRY/atlas-ce/tensorboard-server:$build_version $NEXUS_DOCKER_REGISTRY/atlas-ce/tensorboard-server:latest
