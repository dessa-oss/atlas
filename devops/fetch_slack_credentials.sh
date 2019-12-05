#!/bin/bash

export FOUNDATIONS_SLACK_TOKEN=$(kubectl get secret -n ci-pipeline foundations-slack-token -o yaml | grep '==' | awk '{print $2}' | base64 --decode)
export FOUNDATIONS_TESTING_SLACK_TOKEN=$(kubectl get secret -n ci-pipeline foundations-testing-slack-token -o yaml | grep '==' | awk '{print $2}' | base64 --decode)