#!/bin/bash

# download foundations package to be included in the docker image
pip_version=`../../foundations_contrib/src/foundations_contrib/resources/get_version.sh`
export build_version=`echo $pip_version | sed 's/+/_/g'`

rm -rf tmp/pip_wheels && \
    mkdir -p tmp/pip_wheels && \
    pip download --dest tmp/pip_wheels foundations-rest-api==$pip_version

docker build --tag docker.shehanigans.net/foundations-model-package .

# rm -rf tmp/pip_wheels