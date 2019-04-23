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
    python -m pip install -U $wheel_path
    mkdir ${cwd}/dist 2>/dev/null
    cp $wheel_path ${cwd}/dist
}

cwd=`pwd`

build_module foundations_spec foundations_spec $cwd && \
    build_module foundations_events foundations_events $cwd && \
    build_module foundations_internal foundations_internal $cwd && \
    build_module foundations_contrib foundations_contrib $cwd && \
    build_module foundations_sdk foundations $cwd && \
    build_module gcp_utils foundations_gcp $cwd && \
    build_module ssh_utils foundations_ssh $cwd && \
    build_module aws_utils foundations_aws $cwd && \
    build_module foundations_scheduler_plugin foundations_scheduler_plugin $cwd && \
    build_module foundations_rest_api foundations_rest_api $cwd && \
    build_module foundations_production foundations_production $cwd
