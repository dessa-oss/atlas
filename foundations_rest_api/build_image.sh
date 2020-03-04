#!/bin/bash

docker_image="foundations-rest-api"
docker_registry=${DOCKER_REGISTRY:-docker.shehanigans.net}
pip_build_version=`python get_version.py`
docker_build_version=$(echo $pip_build_version | sed 's/+/_/g')
curr=$(pwd)

image_tag=${docker_registry}/${docker_image}:${docker_build_version}
image_tag_latest=${docker_registry}/${docker_image}:latest

rm -rf tmp/pip_wheels && \
    mkdir -p tmp/pip_wheels && \
    cp dist/* tmp/pip_wheels && \
    docker build \
        -t ${image_tag} \
        --network=host \
        --file foundations_rest_api/Dockerfile \
        --build-arg main_file=run_api_server.py \
        . &&

    docker tag \
        image_tag \
        image_tag_latest &&

echo "Successfully built image tagged to ${docker_build_version} and latest" ||
    echo "Failed to built image"
