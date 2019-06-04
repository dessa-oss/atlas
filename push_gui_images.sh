#!/bin/bash

python -m pip install setuptools_scm

build_version=`python get_version.py | sed 's/+/_/g'`

if [ $? -eq 0 ]
then
    docker push docker.shehanigans.net/foundations-rest-api:${build_version} && \
        docker push docker.shehanigans.net/foundations-rest-api:latest && \
        docker push docker.shehanigans.net/foundations-gui:${build_version} && \
        docker push docker.shehanigans.net/foundations-gui:latest
fi
