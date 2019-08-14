#!/bin/bash
export namespace="foundations-scheduler-test"
export project_name=$1
export model_name=$2
no_follow=$3

envsubst < kubernetes-deployment.envsubst.yaml | kubectl create -f -
echo "Preparing $model_name for serving"

python ingress_modifier.py $project_name $model_name

model_pod=$(kubectl -n $namespace get po | grep $project_name-$model_name | awk '{print $1}')

model_status () {
    echo $(kubectl -n $namespace get po | grep $project_name-$model_name | awk '{print $3}')
}

echo "Waiting for $model_name to be ready"
while [[ "Pending" == $(model_status) ]] || [[ "" == $(model_status) ]] || [[ "ContainerCreating" == $(model_status) ]]
do 
    printf "*"
    sleep 2
done

echo ''
echo Model $model_name has started, please run:
echo -e '    ' foundations serve stop $model_name 
echo if an error has occurred or you wish to stop the server
echo ''
if [[ -z $no_follow ]]; then
    kubectl logs -f -n $namespace $model_pod
fi
    