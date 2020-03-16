#!/bin/bash

export pip_build_version=$(python get_version.py)
export build_version=$pip_build_version
export docker_build_version=$(echo $pip_build_version | sed 's/+/_/g')

wheel_suffix=$(python -c "import sys; print(sys.version_info.major)")
wheel_name_tail="${pip_build_version}-py${wheel_suffix}-none-any.whl"


build_module () {
    directory=$1
    module_name=$2
    cwd=$3
    wheel_path="${cwd}/${directory}/dist/${module_name}-${wheel_name_tail}"
    cd ${cwd}/${directory} && \
    rm -rf "./build" || true && \
    rm -rf "./dist" || true && \
    python setup.py sdist bdist_wheel && \
    python -m pip install -U $wheel_path && \
    cd .. && \
    mkdir -p ${cwd}/dist 2>/dev/null && \
    cp $wheel_path ${cwd}/dist
}