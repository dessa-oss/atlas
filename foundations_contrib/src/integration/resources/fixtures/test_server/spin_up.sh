#!/bin/bash
docker build -t test-server:latest integration/resources/fixtures/test_server/

kubectl apply -f integration/resources/fixtures/test_server/ingress-controller-mandatory.yaml
kubectl apply -f integration/resources/fixtures/test_server/ingress-controller.yaml
kubectl apply -f integration/resources/fixtures/test_server/deployment.yaml
