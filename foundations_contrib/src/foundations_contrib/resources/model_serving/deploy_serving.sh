#!/bin/bash
export model_number=$(head /dev/urandom | LC_CTYPE=C tr -dc 0-9 | head -c 4 ; echo '')
export job_id=$1
export model_name=model-$model_number

cat kubernetes-deployment.envsubst.yaml | envsubst | kubectl create -f -
echo "Preparing $model_name for serving"

model_pod=$(kubectl -n foundations-scheduler-test get po | grep $model_name | awk '{print $1}')

model_status () {
    echo $(kubectl -n foundations-scheduler-test get po | grep $model_name | awk '{print $3}')
}

echo "Waiting for $model_name to be ready"
while [ "Pending" == $(model_status) ] || [ "" == $(model_status) ] || [ "ContainerCreating" == $(model_status) ]
do 
    sleep 2
done

echo Model $model_name has started
kubectl logs -f -n foundations-scheduler-test $model_pod