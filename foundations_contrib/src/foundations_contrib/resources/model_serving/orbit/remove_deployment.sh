#!/bin/bash
kubectl delete deployment -n ingress-nginx $1-$2-deployment && \
    kubectl delete svc -n ingress-nginx $1-$2-service