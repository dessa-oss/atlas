#!/bin/bash

gui_docker_image="foundations-rest-api"
docker_registry="docker.shehanigans.net"
pip_build_version=`python get_version.py`
docker_build_version=$(echo $pip_build_version | sed 's/+/_/g')
curr=$(pwd)

gui_image_tag=${docker_registry}/${gui_docker_image}:${docker_build_version}

rm -rf tmp/pip_wheels && \
    mkdir -p tmp/pip_wheels && \
    cp dist/* tmp/pip_wheels && \
    docker build \
        -t ${gui_image_tag} \
        --network=host \
        --file foundations_rest_api/Dockerfile \
        --build-arg main_file=run_api_server.py \
        .
