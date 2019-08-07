#!/bin/bash
docker build -f integration/fixtures/query_job/Dockerfile -t query-job-python:latest integration/fixtures/query_job/
docker build -f integration/fixtures/hello_server/Dockerfile -t hello-server:latest integration/fixtures/hello_server/

kubectl apply -f integration/fixtures/query_job.yaml
kubectl apply -f integration/fixtures/hello_server.yaml