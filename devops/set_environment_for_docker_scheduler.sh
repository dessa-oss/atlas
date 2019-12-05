#!/bin/bash

export REDIS_URL=redis://localhost:6379
export FOUNDATIONS=${FOUNDATIONS_HOME:-~/.foundations}

export ATLAS_PORT=37722
export ORBIT_PORT=37222
export SCHEDULER_PORT=5000

export FOUNDATIONS_SCHEDULER_URL=http://localhost:${SCHEDULER_PORT}
export LOCAL_DOCKER_SCHEDULER_HOST=localhost
export REMOTE_FOUNDATIONS_HOME=$FOUNDATIONS

export REDIS_HOST=localhost
export REDIS_PORT=6379
export ARCHIVE_DIR=$FOUNDATIONS/job_data
export WORKING_DIR=$FOUNDATIONS/local_docker_scheduler/work_dir
export JOB_BUNDLE_STORE_DIR=$FOUNDATIONS/job_bundle_store_dir
export NUM_WORKERS=0