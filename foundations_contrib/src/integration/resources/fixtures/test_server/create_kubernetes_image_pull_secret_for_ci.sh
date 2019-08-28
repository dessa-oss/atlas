#!/bin/bash

if [[ $# -ne 3 ]]
then
    echo "Usage $0 <kubernetes namespace> <user> <password>" 
    exit 1
else
    namespace=$1
    user=$2
    password=$3
fi

kubectl get --namespace $namespace secret dessa-registry-credentials 2>&1 > /dev/null
exists=$?
if [[ $exists -ne 0 ]]; then
    kubectl create --namespace $namespace \
        secret docker-registry dessa-registry-credentials \
        --docker-server=docker.shehanigans.net \
        --docker-username=$user \
        --docker-password=$password \
        --docker-email=devops@dessa.com
fi