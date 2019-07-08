#!/bin/bash
kubectl delete deployment -n foundations-scheduler-test foundations-model-package-deployment-$1 && \
    kubectl delete svc -n foundations-scheduler-test foundations-model-package-deployment-$1