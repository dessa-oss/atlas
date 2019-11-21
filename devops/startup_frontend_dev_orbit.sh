#!/bin/bash

source dev_env.sh
export REDIS_URL=redis://localhost:6379
export FOUNDATIONS=~/.foundations

export ATLAS_PORT=37722
export ORBIT_PORT=37222
export SCHEDULER_PORT=5000

export FOUNDATIONS_SCHEDULER_URL=localhost:${SCHEDULER_PORT}

export REDIS_HOST=localhost
export REDIS_PORT=6379
export ARCHIVE_DIR=$FOUNDATIONS/job_data
export WORKING_DIR=$FOUNDATIONS/local_docker_scheduler/work_dir
export JOB_BUNDLE_STORE_DIR=$FOUNDATIONS/job_bundle_store_dir
export NUM_WORKERS=0

export REACT_APP_API_URL="http://127.0.0.1:${ORBIT_PORT}/api/v1/"
export REACT_APP_ATLAS_URL="http://127.0.0.1:${ATLAS_PORT}/api/v2beta/"
export REACT_APP_APIARY_URL="http://private-d03986-iannelladessa.apiary-mock.com/api/v1/"

./devops/teardown_frontend_dev_orbit.sh

echo "Note: Ensure you have redis running on port ${REDIS_PORT}"

echo "Running Atlas REST API on port ${ATLAS_PORT}"
python devops/startup_atlas_api.py ${ATLAS_PORT} > $FOUNDATIONS/logs/atlas_rest_api.log 2>&1 &

echo "Running Orbit REST API on port ${ORBIT_PORT}"
python devops/startup_orbit_api.py ${ORBIT_PORT} > $FOUNDATIONS/logs/atlas_rest_api.log 2>&1 &

echo "Running local docker scheduler on port ${SCHEDULER_PORT}"
cd ../local-docker-scheduler && python -m local_docker_scheduler -p ${SCHEDULER_PORT} > $FOUNDATIONS/logs/scheduler.log 2>&1 &

echo Running UI on port 3000
cd foundations_ui_orbit && \
  yarn install && \
  yarn start