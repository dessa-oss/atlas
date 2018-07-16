#!/bin/bash

wheel_suffix=`python -c "import sys; print(sys.version_info.major)"`

cd foundations_sdk/ && \
    python setup.py sdist bdist_wheel && \
    cd ../ && \
    python -m pip install -U foundations_sdk/dist/foundations-0.0.1-py${wheel_suffix}-none-any.whl && \
    cd gcp_utils/ && \
    python setup.py sdist bdist_wheel && \
    cd ../ && \
    python -m pip install -U gcp_utils/dist/foundations_gcp-0.0.1-py${wheel_suffix}-none-any.whl && \
    cd ssh_utils/ && \
    python setup.py sdist bdist_wheel &&\
    cd ../ && \
    python -m pip install -U ssh_utils/dist/foundations_ssh-0.0.1-py${wheel_suffix}-none-any.whl
