#!/bin/bash

python -m pip install setuptools_scm docker

pip_version=`python get_version.py`
export build_version=`echo $pip_version | sed 's/+/_/g'`

script_location="`pwd`/devops/build_scripts"

if [ $? -eq 0 ]
then
    rm -rf tmp/pip_wheels && \
        mkdir -p tmp/pip_wheels && \
        cp dist/* tmp/pip_wheels && \
        cp docker/gui_ce_Dockerfile foundations_ui && \
        python $script_location/gui_and_rest_apis/build_gui_ce.py && \
        rm -rf foundations_ui/gui_ce_Dockerfile
fi
