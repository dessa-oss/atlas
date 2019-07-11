#!/bin/bash
export model_number=$(head /dev/urandom | LC_CTYPE=C tr -dc 0-9 | head -c 4 ; echo '')
export job_id=$1
export model_name=model-$model_number

cat kubernetes-deployment.envsubst.yaml | envsubst | kubectl create -f -
echo Model $model_name serving, stuff cole says

sleep 15
model_pod=$(kubectl get po -n foundations-scheduler-test | grep $model_name | awk '{print $1}')

model_status () {
    return $(kubectl get po -n foundations-scheduler-test | grep $model_name | awk '{print $3}')
}

while [ "Running" != model_status ]
do 
    sleep 2
done

kubectl logs -f -n foundations-scheduler-test $model_pod