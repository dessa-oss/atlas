#!/bin/bash

export build_version=`python get_version.py | sed 's/+/_/g'`
registry=${NEXUS_DOCKER_REGISTRY:-docker.shehanigans.net}
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker build --network=host -t "$registry/auth-server:$build_version" $DIR \
  && docker tag "$registry/auth-server:$build_version" "$registry/auth-server:latest" \
  && docker push "$registry/auth-server" \
  && echo "Successfully build and pushed auth-server to the $registry repository"
