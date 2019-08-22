#!/bin/bash

kubectl config set-context kubernetes-admin@kubernetes 

kubectl delete -f integration/resources/fixtures/test_server/ingress.yaml && \
kubectl delete -f integration/resources/fixtures/test_server/ingress-controller.yaml && \
kubectl delete -f integration/resources/fixtures/test_server/ingress-controller-mandatory.yaml 
