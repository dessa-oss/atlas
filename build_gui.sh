#!/bin/bash

python -m pip install setuptools_scm

build_version=`python get_version.py | sed 's/+/_/g'`


if [ $? -eq 0 ]
then
    rm -rf tmp/pip_wheels && \
        mkdir -p tmp/pip_wheels && \
        pip download --dest tmp/pip_wheels foundations_rest_api && \
        docker build . -f docker/rest_api_Dockerfile -t docker.shehanigans.net/foundations-rest-api:${build_version} && \
        docker tag docker.shehanigans.net/foundations-rest-api:${build_version} docker.shehanigans.net/foundations-rest-api:latest && \
        docker build foundations_ui -f docker/gui_Dockerfile -t docker.shehanigans.net/foundations-gui:${build_version} && \
        docker tag docker.shehanigans.net/foundations-gui:${build_version} docker.shehanigans.net/foundations-gui:latest
fi