#!/bin/bash

attempt_counter=0
SERVICE=$1
max_attempts=$2

until $(curl --output /dev/null --silent --head --fail $SERVICE); do
    if [ ${attempt_counter} -eq ${max_attempts} ];then
      echo "Max attempts reached"
      exit 1
    fi

    printf '.'
    attempt_counter=$(($attempt_counter+1))
    sleep 1
done

echo "Connection $SERVICE found"