#!/bin/bash
kubectl delete deployment -n foundations-scheduler-test $1-$2-deployment && \
    kubectl delete svc -n foundations-scheduler-test $1-$2-service