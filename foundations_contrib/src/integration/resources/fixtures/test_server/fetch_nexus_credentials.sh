#!/bin/bash

if [[ -z "$NEXUS_PASSWORD" ]]; then
    if [[ $# -ne 2 ]]
    then
        echo "Usage $0 <kubernetes namespace> <nexus user>" 
        exit 1
    else
        namespace=$1
        user=$2
    fi

    current_context=`kubectl config current-context`
    kubectl config use-context arn:aws:eks:us-east-1:451430605210:cluster/devops > /dev/null 
    secret=$(kubectl get secret --namespace $namespace $user-password -o go-template={{.data.password}} | base64 --decode)
    success=$?
    echo "$secret"
    kubectl config use-context $current_context > /dev/null
    exit $success
else
    echo $NEXUS_PASSWORD
fi