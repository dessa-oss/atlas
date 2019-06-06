#!/bin/bash

python -m pip install setuptools_scm docker

pip_version=`python get_version.py`
export build_version=`echo $pip_version | sed 's/+/_/g'`


if [ $? -eq 0 ]
then
    rm -rf tmp/pip_wheels && \
        mkdir -p tmp/pip_wheels && \
        pip download --dest tmp/pip_wheels foundations_rest_api==$pip_version && \
        cp docker/gui_Dockerfile foundations_ui && \
        python build_gui.py
    rm foundations_ui/gui_Dockerfile
fi