#!/bin/bash

export FOUNDATIONS=${FOUNDATIONS_HOME:-~/.foundations}

export ATLAS_PORT=${ATLAS_PORT:-37722}
export ORBIT_PORT=${ORBIT_PORT:-37222}

export SCHEDULER_PORT=${SCHEDULER_PORT:-5000}
export SCHEDULER_HOST=${SCHEDULER_HOST:-localhost}
export FOUNDATIONS_SCHEDULER_URL=http://${SCHEDULER_HOST}:${SCHEDULER_PORT}

export REDIS_HOST=${REDIS_HOST:-localhost}
export REDIS_PORT=${REDIS_PORT:-6379}
export REDIS_URL="redis://$REDIS_HOST:$REDIS_PORT"

export F9S_LOG_DIR=$FOUNDATIONS/logs
mkdir -p $F9S_LOG_DIR

export ARCHIVE_DIR=$FOUNDATIONS/job_data
mkdir -p $ARCHIVE_DIR

export WORKING_DIR=$FOUNDATIONS/local_docker_scheduler/work_dir
mkdir -p $WORKING_DIR

export JOB_BUNDLE_STORE_DIR=$FOUNDATIONS/job_bundle_store_dir
mkdir -p $JOB_BUNDLE_STORE_DIR

export NUM_WORKERS=0

export REACT_APP_API_URL="http://127.0.0.1:${ORBIT_PORT}/api/v1/"
export REACT_APP_ATLAS_URL="http://127.0.0.1:${ATLAS_PORT}/api/v2beta/"
export REACT_APP_APIARY_URL="http://private-d03986-iannelladessa.apiary-mock.com/api/v1/"

export LOCAL_DOCKER_SCHEDULER_DIR=../local-docker-scheduler

export LOCAL_DOCKER_SCHEDULER_HOST=${LOCAL_DOCKER_SCHEDULER_HOST:-localhost}
export REMOTE_FOUNDATIONS_HOME=${REMOTE_FOUNDATIONS_HOME:-$FOUNDATIONS}