#!/bin/bash

kubectl delete -f integration/fixtures/hello_server.yaml
kubectl delete -f integration/fixtures/query_job.yaml