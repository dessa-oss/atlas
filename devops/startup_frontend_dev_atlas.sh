#!/bin/bash

source activate_dev_env.sh
export FOUNDATIONS=${FOUNDATIONS_HOME:-~/.foundations}

export ATLAS_PORT=37722
export AUTH_PROXY_PORT=5558
export SCHEDULER_PORT=5000
export FOUNDATIONS_SCHEDULER_URL=http://localhost:${SCHEDULER_PORT}
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_URL="redis://$REDIS_HOST:$REDIS_PORT"

export ARCHIVE_DIR=$FOUNDATIONS/job_data
mkdir -p ARCHIVE_DIR

export WORKING_DIR=$FOUNDATIONS/local_docker_scheduler/work_dir
mkdir -p WORKING_DIR

export JOB_BUNDLE_STORE_DIR=$FOUNDATIONS/job_bundle_store_dir
mkdir -p $JOB_BUNDLE_STORE_DIR

export NUM_WORKERS=1

export REACT_APP_ATLAS_URL="http://127.0.0.1:${AUTH_PROXY_PORT}/api/v2beta/"
export REACT_APP_APIARY_URL="http://private-d03986-iannelladessa.apiary-mock.com/api/v1/"
export REACT_APP_API_STAGING_URL="http://localhost:5558/api/v2beta/"

./devops/teardown_frontend_dev_atlas.sh

echo "Note: Ensure you have redis running and accessible at ${REDIS_URL}"

echo "Running Atlas REST API on port ${ATLAS_PORT}"
python devops/startup_atlas_api.py ${ATLAS_PORT} &

echo "Attempting to run scheduler with foundations home set to $FOUNDATIONS"

cd ../local-docker-scheduler \
  && pip install -r requirements.txt \
  && python -m local_docker_scheduler -p ${SCHEDULER_PORT} > $FOUNDATIONS/logs/scheduler.log 2>&1 &

cd ../foundations-auth-proxy \
&& pip install -r requirements.txt \
&& python -m auth_proxy -n -p 5558 --dev > $FOUNDATIONS/logs/auth_proxy.log 2>&1 &

cd foundations_ui && \
  echo "Install UIs dependencies" && \
  yarn install && \
  echo "Starting the UI in development mode with yarn" && \
  yarn start > $FOUNDATIONS/logs/yarn.log 2>&1 &

./foundations_contrib/src/foundations_contrib/authentication/launch.sh
docker run --name redis --rm -d -p 6379:6379 redis

echo "Running UI on port 3000"

echo "Check log files for status of programs:"
echo "    $FOUNDATIONS/logs/scheduler.log"
echo "    $FOUNDATIONS/logs/yarn.log"
echo "    $FOUNDATIONS/logs/orbit_rest_api.log"
