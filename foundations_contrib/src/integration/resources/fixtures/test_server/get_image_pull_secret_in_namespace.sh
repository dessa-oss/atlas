#!/bin/bash

context='arn:aws:eks:us-east-1:451430605210:cluster/devops'
namespace='ingress-nginx-test'

current_context=`kubectl config current-context`
kubectl config use-context $context > /dev/null 
./integration/resources/fixtures/test_server/create_kubernetes_image_pull_secret_for_ci.sh $namespace jenkins-user `./integration/resources/fixtures/test_server/fetch_nexus_credentials.sh ci-pipeline jenkins-user`
success=$?
kubectl config use-context $current_context > /dev/null
exit $success