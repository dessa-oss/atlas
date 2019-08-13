#!/bin/bash

current_context=`kubectl config current-context`
namespace='ingress-nginx-test'

kubectl config use-context $current_context > /dev/null
./integration/resources/fixtures/test_server/create_kubernetes_image_pull_secret_for_ci.sh $namespace jenkins-user `./integration/resources/fixtures/test_server/fetch_nexus_credentials.sh ci-pipeline jenkins-user`
success=$?
exit $success