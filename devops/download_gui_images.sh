#!/bin/bash

build_version=`python get_version.py`

docker pull docker.shehanigans.net/foundations-rest-api:${build_version} && \
    docker pull docker.shehanigans.net/foundations-gui:${build_version}