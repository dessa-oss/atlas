#!/bin/bash

build_version=`./docker_image_version.sh`

docker pull docker.shehanigans.net/foundations-rest-api:${build_version} && \
    docker pull docker.shehanigans.net/foundations-gui:${build_version}