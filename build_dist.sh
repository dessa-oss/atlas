#!/bin/bash

wheel_suffix=`python -c "import sys; print(sys.version_info.major)"`

export build_version=0.0.4

cd foundations_sdk/ && \
    python setup.py sdist bdist_wheel && \
    cd ../ && \
    python -m pip install -U foundations_sdk/dist/foundations-${build_version}-py${wheel_suffix}-none-any.whl && \
    cd gcp_utils/ && \
    python setup.py sdist bdist_wheel && \
    cd ../ && \
    python -m pip install -U gcp_utils/dist/foundations_gcp-${build_version}-py${wheel_suffix}-none-any.whl && \
    cd ssh_utils/ && \
    python setup.py sdist bdist_wheel &&\
    cd ../ && \
    python -m pip install -U ssh_utils/dist/foundations_ssh-${build_version}-py${wheel_suffix}-none-any.whl && \
    cd aws_utils/ && \
    python setup.py sdist bdist_wheel &&\
    cd ../ && \
    python -m pip install -U aws_utils/dist/foundations_aws-${build_version}-py${wheel_suffix}-none-any.whl
