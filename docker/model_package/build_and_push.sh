#!/bin/bash

docker build --tag docker.shehanigans.net/foundations-model-package . && \
    docker push docker.shehanigans.net/foundations-model-package