#!/bin/bash

job_id=$1

kubectl delete fndj -n foundations-scheduler-test $job_id --grace-period 0 --force && \
    kubectl delete job -n foundations-scheduler-test foundations-job-$job_id --grace-period 0 --force