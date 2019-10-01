#!/bin/bash

export namespace=$1
export project_name=$2
export model_name=$3

model_status () {
    echo $(kubectl -n $namespace get po | grep $project_name-$model_name | awk '{print $3}')
}

envsubst < integration/resources/fixtures/test_server/test-server-deployment-and-service.yaml | kubectl apply -f - && \
    envsubst < foundations_contrib/resources/model_serving/ingress.envsubst.yaml | kubectl apply -f - > /dev/null 2>&1

status=$?

if [[ $status -ne 0 ]]
then
    exit $status
fi
 
kubectl -n $namespace get ingress foundations-model-package-${project_name}-ingress > /dev/null 2>&1

if [[ $? -ne 0 ]]
then
    envsubst < foundations_contrib/resources/model_serving/project-ingress.envsubst.yaml | kubectl apply -f - > /dev/null 2>&1
    status=$?
fi


while [ "Pending" == $(model_status) ] || [ "" == $(model_status) ] || [ "ContainerCreating" == $(model_status) ]
do 
    sleep 2
done

exit $status