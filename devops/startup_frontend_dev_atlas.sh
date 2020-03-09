#!/bin/bash

export SCRIPT_PID=$$
export F9S_ENV_TYPE="atlas"

source activate_dev_env.sh
source ./devops/set_environment_for_dev.sh

export REACT_APP_API_URL="http://127.0.0.1:${AUTH_PROXY_PORT}/api/v1/"
export REACT_APP_API_STAGING_URL="http://localhost:${AUTH_PROXY_PORT}/api/v2beta/"

# ***************************************************************************************************************

check_for_config_and_create_if_does_not_exists "execution"
check_for_config_and_create_if_does_not_exists "submission"
check_for_config_and_create_if_does_not_exists "worker_execution"
check_for_config_and_create_if_does_not_exists "worker_submission"

# ***************************************************************************************************************

echo " Ensuring stoping previous running altas"
./devops/teardown_frontend_dev_atlas.sh

# ***************************************************************************************************************

echo "Attempting to run redis at ${REDIS_PORT}. NB If redis is already running port flag will not have an effect"
source ./devops/start_redis.sh atlas $REDIS_PORT

# Place wait for port script in a better locations
# echo "Waiting for redis to start at redis://${REDIS_HOST}:${REDIS_PORT}"
# ./devops/wait_for_url.sh $REDIS_HOST $REDIS_PORT 50 # Only works for HTTP ports

# ***************************************************************************************************************

echo "Running Atlas REST API on port ${ATLAS_PORT}"
python devops/startup_atlas_api.py ${ATLAS_PORT} &

echo "Waiting for Atlas REST API to start at http://localhost:${ATLAS_PORT}"
./devops/wait_for_url.sh "http://localhost:${ATLAS_PORT}/api/v2beta/projects" 10

check_status_of_process "Atlas REST API" $? $SCRIPT_PID

# ***************************************************************************************************************

echo "Starting the Scheduler ......."
start_scheduler

echo "Waiting for Scheduler to start at http://localhost:${SCHEDULER_PORT}"
./devops/wait_for_url.sh "http://localhost:${SCHEDULER_PORT}" 10

check_status_of_process "Scheduler" $? $SCRIPT_PID

# ***************************************************************************************************************

echo "Starting Auth Proxy ....."
start_auth_proxy $F9S_ENV_TYPE

echo "Waiting for Auth Proxy to start at http://localhost:${AUTH_PROXY_PORT}"
./devops/wait_for_url.sh "http://localhost:${AUTH_PROXY_PORT}" 10

check_status_of_process "Auth Proxy" $? $SCRIPT_PID

# ***************************************************************************************************************

echo "Starting the Auth Server (keycloak) ....." 
start_auth_server $F9S_ENV_TYPE

echo "Waiting for Auth Server to start at http://localhost:8080"
./devops/wait_for_url.sh "http://localhost:8080" 80

check_status_of_process "Auth Server" $? $SCRIPT_PID

# ***************************************************************************************************************

cd foundations_ui && \
  echo "Install UIs dependencies" && \
  yarn install --silent 2> >(grep -v warning 1>&2) && \
  echo "Starting the UI in development mode with yarn" && \
  yarn start > $FOUNDATIONS_HOME/logs/yarn.log 2>&1 &

echo "Waiting for Atlas GUI to start at http://localhost:${GUI_PORT}"
./devops/wait_for_url.sh "http://localhost:${GUI_PORT}" 80

check_status_of_process "Atlas GUI" $? $SCRIPT_PID

# ***************************************************************************************************************

echo "Check log files for status of programs:"
echo "    tail -f $FOUNDATIONS_HOME/logs/scheduler.log"
echo "    tail -f $FOUNDATIONS_HOME/logs/yarn.log"
echo "    tail -f $FOUNDATIONS_HOME/logs/atlas_rest_api.log"
echo "    tail -f $FOUNDATIONS_HOME/logs/auth_proxy.log"
echo "    docker logs -f ${AUTH_SERVER_NAME}"