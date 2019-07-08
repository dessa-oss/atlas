#!/bin/bash
export model_number=$(head /dev/urandom | LC_CTYPE=C tr -dc 0-9 | head -c 4 ; echo '')
export job_id=$1
export model_name=model-$model_number

cat kubernetes-deployment.envsubst.yaml | envsubst | kubectl create -f -