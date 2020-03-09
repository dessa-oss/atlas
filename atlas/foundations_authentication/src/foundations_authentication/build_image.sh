#!/bin/bash

# NB: File is expected to be executed from root of project

docker_image="auth-server"
docker_registry=${DOCKER_REGISTRY:-docker.shehanigans.net}
pip_build_version=`python get_version.py`
docker_build_version=$(echo $pip_build_version | sed 's/+/_/g')

image_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

image_tag=${docker_registry}/${docker_image}:${docker_build_version}
image_tag_latest=${docker_registry}/${docker_image}:latest

docker build \
    -t ${image_tag} \
    --network=host \
    ${image_dir} &&

docker tag \
    ${image_tag} \
    ${image_tag_latest} &&

echo "Successfully built image ${docker_image} tagged to ${docker_build_version} and latest"
