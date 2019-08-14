#!/bin/bash

export project_name=$1
export model_name=$2
namespace="ingress-nginx-test"

model_status () {
    echo $(kubectl -n $namespace get po | grep $project_name-$model_name | awk '{print $3}')
}

envsubst < integration/resources/fixtures/test_server/test-server-deployment-and-service.yaml | kubectl create -f - && \
python foundations_contrib/resources/model_serving/orbit/ingress_modifier.py $project_name $model_name

while [ "Pending" == $(model_status) ] || [ "" == $(model_status) ] || [ "ContainerCreating" == $(model_status) ]
do 
    sleep 2
done

