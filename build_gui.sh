#!/bin/bash

python -m pip install setuptools_scm docker

pip_version=`foundations_contrib/src/foundations_contrib/resources/get_version.sh`
export build_version=`echo $pip_version | sed 's/+/_/g'`


if [ $? -eq 0 ]
then
    rm -rf tmp/pip_wheels && \
        mkdir -p tmp/pip_wheels && \
        pip download --dest tmp/pip_wheels foundations-rest-api==$pip_version && \
        cp docker/gui_Dockerfile foundations_ui && \
        python build_gui.py && \
        rm -rf foundations_ui/gui_Dockerfile
fi