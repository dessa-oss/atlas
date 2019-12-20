#!/bin/bash

source activate_dev_env.sh
source ./devops/set_environment_for_docker_scheduler.sh

export REACT_APP_ATLAS_URL="http://127.0.0.1:${AUTH_PROXY_PORT}/api/v2beta/"
export REACT_APP_APIARY_URL="http://private-d03986-iannelladessa.apiary-mock.com/api/v1/"
export REACT_APP_API_STAGING_URL="http://localhost:5558/api/v2beta/"


echo "Ensuring that orbit is not also running"
./devops/teardown_frontend_dev_orbit.sh

echo " Ensuring stoping previous running altas"
./devops/teardown_frontend_dev_atlas.sh

echo "Attempting to run redis at ${REDIS_PORT}. NB If redis is already running port flag will not have an effect"
./devops/start_redis.sh atlas $REDIS_PORT

echo "Running Atlas REST API on port ${ATLAS_PORT}"
python devops/startup_atlas_api.py ${ATLAS_PORT} &

echo "Starting the Scheduler ......."
start_scheduler

echo "Starting Auth Proxy ....."
start_auth_proxy

echo "Starting the Auth Server (keycloak) ....." 
start_auth_server

cd foundations_ui && \
  echo "Install UIs dependencies" && \
  yarn install && \
  echo "Starting the UI in development mode with yarn" && \
  yarn start > $FOUNDATIONS_HOME/logs/yarn.log 2>&1 &


echo "Check log files for status of programs:"
echo "    tail -f $FOUNDATIONS_HOME/logs/scheduler.log"
echo "    tail -f $FOUNDATIONS_HOME/logs/yarn.log"
echo "    tail -f $FOUNDATIONS_HOME/logs/atlas_rest_api.log"
echo "    tail -f $FOUNDATIONS_HOME/logs/auth_proxy.log"
echo "    docker logs -f ${AUTH_SERVER_NAME}"