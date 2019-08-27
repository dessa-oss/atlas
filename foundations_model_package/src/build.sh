#!/bin/bash

# download foundations package to be included in the docker image

if [ "$RUNNING_ON_CI" != "TRUE" ]; then
    cwd=$(pwd)
    cd ../..
    ./build_dist.sh
    cd $cwd
fi

pip_version=`../../foundations_contrib/src/foundations_contrib/resources/get_version.sh`
export build_version=`echo $pip_version | sed 's/+/_/g'`

rm -rf tmp/pip_wheels && \
    mkdir -p tmp/pip_wheels && \
    cp ../../dist/* tmp/pip_wheels && \
    python -m pip download --find-links=tmp/pip_wheels foundations-rest-api==${pip_version} --dest tmp/pip_wheels

image_name=docker.shehanigans.net/foundations-model-package

docker build --tag ${image_name}:${build_version} .
docker tag ${image_name}:${build_version} ${image_name}:latest
docker tag ${image_name}:${build_version} docker-staging.shehanigans.net/foundations-model-package:latest