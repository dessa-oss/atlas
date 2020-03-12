#!/bin/bash

repo=$1
tag=$2

pip_version=`python get_version.py`
export build_version=`echo $pip_version | sed 's/+/_/g'`
export NEXUS_DOCKER_REGISTRY=${NEXUS_DOCKER_REGISTRY:-us.gcr.io/atlas}

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker build --network=host -t $NEXUS_DOCKER_REGISTRY/tensorboard-rest-api:$build_version $DIR \
    && docker tag $NEXUS_DOCKER_REGISTRY/tensorboard-rest-api:$build_version \
        $NEXUS_DOCKER_REGISTRY/tensorboard-rest-api:latest
