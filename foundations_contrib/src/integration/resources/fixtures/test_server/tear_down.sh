#!/bin/bash

export project_name=$1

kubectl -n foundations-scheduler-test delete ingress foundations-model-package-${project_name}-ingress
kubectl config set-context kubernetes-admin@kubernetes