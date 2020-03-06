#!/bin/bash

docker_image="foundations-rest-api"
docker_registry=${DOCKER_REGISTRY:-docker.shehanigans.net}
pip_build_version=`python get_version.py`
docker_build_version=$(echo $pip_build_version | sed 's/+/_/g')
curr="$(pwd)/atlas"

image_tag=${docker_registry}/${docker_image}:${docker_build_version}
image_tag_latest=${docker_registry}/${docker_image}:latest

rm -rf "${curr}/tmp/pip_wheels" && \
    mkdir -p "${curr}/tmp/pip_wheels" && \
    cp ${curr}/dist/* ${curr}/tmp/pip_wheels && \
    docker build \
        -t ${image_tag} \
        --network=host \
        --file ${curr}/foundations_rest_api/Dockerfile \
        --build-arg main_file=run_api_server.py \
        ${curr} && \

    docker tag \
        ${image_tag} \
        ${image_tag_latest} && \

echo "Successfully built image tagged to ${docker_build_version} and latest"
