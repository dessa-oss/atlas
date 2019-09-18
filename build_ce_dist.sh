#!/bin/bash

wheel_suffix=`python -c "import sys; print(sys.version_info.major)"`

python -m pip install setuptools_scm
export build_version=`python get_version.py`

wheel_name_tail="${build_version}-py${wheel_suffix}-none-any.whl"

build_module () {
    directory=$1
    module_name=$2
    cwd=$3
    wheel_path=${directory}/dist/${module_name}-${wheel_name_tail}

    cd ${directory} && \
        python setup.py sdist bdist_wheel && \
        cd .. && \
        mkdir -p ${cwd}/dist 2>/dev/null && \
        cp $wheel_path ${cwd}/dist
}

cwd=`pwd`

rm -rf dist/* && \
    build_module foundations_internal foundations_internal $cwd && \
    build_module foundations_events foundations_events $cwd && \
    build_module foundations_contrib foundations_contrib $cwd && \
    build_module foundations_local_docker_scheduler_plugin foundations_local_docker_scheduler_plugin $cwd && \
    build_module foundations_sdk dessa_foundations $cwd && \
    build_module foundations_core_rest_api_components foundations_core_rest_api_components $cwd && \
    build_module foundations_rest_api foundations_rest_api $cwd