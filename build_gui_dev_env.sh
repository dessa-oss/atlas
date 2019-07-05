#!/bin/bash

python -m pip install setuptools_scm

pip_version=`foundations_contrib/src/foundations_contrib/resources/get_version.sh`
export build_version=`echo $pip_version | sed 's/+/_/g'`
export NEXUS_DOCKER_REGISTRY='docker.shehanigans.net'

./build_dist.sh

if [ $? -eq 0 ]
then
    rm -rf tmp/pip_wheels && \
        mkdir -p tmp/pip_wheels && \
        cp dist/* tmp/pip_wheels && \
        pip download --dest tmp/pip_wheels foundations-scheduler && \
        cp docker/gui_Dockerfile foundations_ui && \
        python build_gui.py && \
        rm -rf foundations_ui/gui_Dockerfile
fi