#!/bin/bash

kubectl apply -f integration/resources/fixtures/test_server/ingress-controller-mandatory.yaml && \
kubectl apply -f integration/resources/fixtures/test_server/ingress-controller.yaml && \
kubectl apply -f integration/resources/fixtures/test_server/ingress.yaml && \
./integration/resources/fixtures/test_server/get_image_pull_secret_in_namespace.sh
# kubectl apply -f integration/resources/fixtures/test_server/deployment.yaml && \
