#!/bin/bash
kubectl delete -f integration/resources/fixtures/test_server/ingress-controller-mandatory.yaml --grace-period=0 && \
kubectl delete -f integration/resources/fixtures/test_server/ingress-controller.yaml --grace-period=0 && \
kubectl delete -f integration/resources/fixtures/test_server/ingress.yaml --grace-period=0
# kubectl delete -f integration/resources/fixtures/test_server/deployment.yaml
