#!/bin/bash

staging_image='docker-staging.shehanigans.net/foundations-model-package:latest'
remote_command="docker pull ${staging_image} && docker tag ${staging_image} docker.shehanigans.net/foundations-model-package:latest"

kubectl -n kube-system exec $(kubectl -n kube-system get pod -l app=docker-pod-for-jenkins -o go-template="{{(index .items 0).metadata.name}}") -- ash -c "${remote_command}"