#!/bin/bash

python_version=$1

wheel_suffix=""

if [[ "${python_version}" = "python2" ]]
then
    wheel_suffix="py2"
elif [[ "${python_version}" = "python3" ]]
then
    wheel_suffix="py3"
else
    echo "Usage: ./build_dist (python2|python3)"
    exit 1
fi

cd vcat_sdk/ && \
    ./build.sh && \
    cd ../ && \
    ${python_version} -m pip install -U vcat_sdk/dist/vcat-0.0.1-${wheel_suffix}-none-any.whl

cd gcp_utils/ && \
    ./build.sh && \
    cd ../ && \
    ${python_version} -m pip install -U gcp_utils/dist/vcat_gcp-0.0.1-${wheel_suffix}-none-any.whl

cd ssh_utils/ && \
    ./build.sh && \
    cd ../ && \
    ${python_version} -m pip install -U ssh_utils/dist/vcat_ssh-0.0.1-${wheel_suffix}-none-any.whl