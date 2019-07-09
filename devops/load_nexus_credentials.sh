#!/bin/bash

export NEXUS_PASSWORD=$(kubectl get secret -o yaml -n ci-pipeline jenkins-user-password | grep password: | awk '{print $2}' | base64 -d)
export NEXUS_URL=https://nexus.shehanigans.net/repository/dessa-pypi/
export NEXUS_USER=jenkins-user
export NEXUS_DOCKER_REGISTRY=docker.shehanigans.net