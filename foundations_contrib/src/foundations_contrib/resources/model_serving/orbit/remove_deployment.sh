#!/bin/bash
namespace=$1
project=$2
model=$3

kubectl delete deployment -n $namespace $project-$model-deployment
kubectl delete svc -n $namespace $project-$model-service