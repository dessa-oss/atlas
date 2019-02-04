#!/bin/bash

python -m pip install setuptools_scm

build_version=`python get_version.py | sed 's/+/_/g'`

if [ $? -eq 0 ]
then
    docker build . -f docker/rest_api_Dockerfile -t foundations-rest-api:${build_version} && \
    docker tag foundations-rest-api:${build_version} foundations-rest-api:latest && \
    docker build foundations_ui -f docker/gui_Dockerfile -t foundations-gui:${build_version} && \
    docker tag foundations-gui:${build_version} foundations-gui:latest
fi