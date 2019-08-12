#!/bin/bash
namespace="ingress-nginx-test"
project=$1
model=$2

kubectl delete deployment -n $namespace $project-$model-deployment
kubectl delete svc -n $namespace $project-$model-service