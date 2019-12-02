#!/bin/bash

python -m pip install setuptools_scm

pip_version=`python get_version.py`
export build_version=`echo $pip_version | sed 's/+/_/g'`
export NEXUS_DOCKER_REGISTRY=${NEXUS_DOCKER_REGISTRY:-docker.shehanigans.net}

script_location="`pwd`/devops/build_scripts"

$script_location/build_all_dist.sh

if [ $? -eq 0 ]
then
    rm -rf tmp/pip_wheels && \
        mkdir -p tmp/pip_wheels && \
        cp dist/* tmp/pip_wheels && \
        cp docker/gui_Dockerfile foundations_ui && \
       $script_location/helpers/parallel.py "python $script_location/gui_and_rest_apis/build_gui.py atlas" "python $script_location/gui_and_rest_apis/build_gui.py orbit" && \
        rm -rf foundations_ui/gui_Dockerfile
fi