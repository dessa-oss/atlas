#!/bin/bash
namespace='foundations-scheduler-test'
export project_name=$1
export model_name=$2

kubectl -n $namespace delete deployment  foundations-model-package-$project_name-$model_name-deployment
kubectl -n $namespace delete svc foundations-model-package-$project_name-$model_name-service