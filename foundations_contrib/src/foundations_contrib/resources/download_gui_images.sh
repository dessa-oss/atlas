#!/bin/bash

pip_version=`./get_version.sh`
build_version=`echo $pip_version | sed 's/+/_/g'`

docker pull docker.shehanigans.net/foundations-rest-api:${build_version} && \
    docker pull docker.shehanigans.net/foundations-gui:${build_version}