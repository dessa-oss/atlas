#!/bin/bash

wheel_suffix=`python -c "import sys; print(sys.version_info.major)"`

cd vcat_sdk/ && \
    python setup.py sdist bdist_wheel && \
    cd ../ && \
    python -m pip install -U vcat_sdk/dist/vcat-0.0.1-py${wheel_suffix}-none-any.whl && \
    cd gcp_utils/ && \
    python setup.py sdist bdist_wheel && \
    cd ../ && \
    python -m pip install -U gcp_utils/dist/vcat_gcp-0.0.1-py${wheel_suffix}-none-any.whl && \
    cd ssh_utils/ && \
    python setup.py sdist bdist_wheel &&\
    cd ../ && \
    python -m pip install -U ssh_utils/dist/vcat_ssh-0.0.1-py${wheel_suffix}-none-any.whl
