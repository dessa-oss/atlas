#!/bin/bash

echo $(kubectl get services | grep query-job-python-service | awk '{print $3}')