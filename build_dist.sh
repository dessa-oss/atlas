#!/bin/bash

wheel_suffix=`python -c "import sys; print(sys.version_info.major)"`

python -m pip install setuptools_scm
export build_version=`python get_version.py`

wheel_name_tail="${build_version}-py${wheel_suffix}-none-any.whl"

build_module () {
    directory=$1
    module_name=$2

    cd ${directory} && \
    python setup.py sdist bdist_wheel && \
    cd .. && \
    python -m pip install -U ${directory}/dist/${module_name}-${wheel_name_tail}
}

build_module foundations_spec foundations_spec && \
    build_module foundations_events foundations_events && \
    build_module foundations_internal foundations_internal && \
    build_module foundations_contrib foundations_contrib && \
    build_module foundations_sdk foundations && \
    build_module gcp_utils foundations_gcp && \
    build_module ssh_utils foundations_ssh && \
    build_module aws_utils foundations_aws && \
    build_module foundations_scheduler_plugin foundations_scheduler_plugin && \
    build_module foundations_rest_api foundations_rest_api
