#!/bin/bash

source activate_dev_env.sh
source ./devops/set_environment_for_docker_scheduler.sh

export REACT_APP_API_URL="http://127.0.0.1:${ORBIT_PORT}/api/v1/"
export REACT_APP_ATLAS_URL="http://127.0.0.1:${ATLAS_PORT}/api/v2beta/"
export REACT_APP_APIARY_URL="http://private-d03986-iannelladessa.apiary-mock.com/api/v1/"

./devops/teardown_frontend_dev_orbit.sh

echo "Note: Ensure you have redis running and accessible at ${REDIS_URL}"

echo "Running Atlas REST API on port ${ATLAS_PORT}"
python devops/startup_atlas_api.py ${ATLAS_PORT} &

echo "Running Orbit REST API on port ${ORBIT_PORT}"
python devops/startup_orbit_api.py ${ORBIT_PORT} &

echo "Generating database.config.yaml at $FOUNDATIONS_HOME/config/local_docker_scheduler/" \
  && mkdir -p $FOUNDATIONS_HOME/config/local_docker_scheduler \
  && cat ./devops/envsubsts/database.config.envsubst.yaml | envsubst > $FOUNDATIONS_HOME/config/local_docker_scheduler/database.config.yaml \
  && echo '' \
  && echo 'Creating a symbolic link for the scheduler to run locally between $FOUNDATIONS_HOME/config/local_docker_scheduler/database.config.yaml -> $LOCAL_DOCKER_SCHEDULER_DIR/database.config.yaml' \
  && echo '' \
  && rm -f $LOCAL_DOCKER_SCHEDULER_DIR/database.config.yaml \
  && ln -s $FOUNDATIONS_HOME/config/local_docker_scheduler/database.config.yaml $LOCAL_DOCKER_SCHEDULER_DIR/database.config.yaml \
  && echo "Generating tracker.config.yaml at $FOUNDATIONS_HOME/config/local_docker_scheduler/" \
  && cat ./devops/envsubsts/tracker_client_plugins.envsubst.yaml | envsubst > $FOUNDATIONS_HOME/config/local_docker_scheduler/tracker_client_plugins.yaml \
  && echo '' \
  && echo 'Creating a symbolic link for the scheduler to run locally between $FOUNDATIONS_HOME/config/local_docker_scheduler/tracker_client_plugins.yaml -> $LOCAL_DOCKER_SCHEDULER_DIR/tracker_client_plugins.yaml' \
  && echo '' \
  && rm -f $LOCAL_DOCKER_SCHEDULER_DIR/tracker_client_plugins.yaml \
  && ln -s $FOUNDATIONS_HOME/config/local_docker_scheduler/tracker_client_plugins.yaml $LOCAL_DOCKER_SCHEDULER_DIR/tracker_client_plugins.yaml \
  && cd $LOCAL_DOCKER_SCHEDULER_DIR \
  && pip install -r requirements_dev.txt \
  && python -m local_docker_scheduler -p ${SCHEDULER_PORT} > $FOUNDATIONS_HOME/logs/scheduler.log 2>&1 &

echo 'Starting up the auth proxy' \
  && echo '' \
  && cd ../foundations-auth-proxy \
  && pip install -r requirements.txt \
  && python -m auth_proxy -n -p 5558 --dev > $FOUNDATIONS_HOME/logs/auth_proxy.log 2>&1 &

echo "Starting the Auth Server (keycloak)" \
  && echo '' \
  && ./foundations_contrib/src/foundations_contrib/authentication/launch.sh

echo "Ensuring that the docker network is configured for the orbit workers" \
  && echo '' \
  && docker network create foundations-orbit || true \
  && redis_docker_id=$(docker ps --filter "name=redis" --quiet) \
  && docker network connect foundations-orbit $redis_docker_id || true

cd foundations_ui_orbit \
  && echo "Install UI dependencies" \
  && yarn install \
  && echo "Starting the UI in development mode with yarn" \
  && yarn start > $FOUNDATIONS_HOME/logs/yarn.log 2>&1 &

echo "Running UI on port 3000"

echo "Check log files for status of programs:"
echo "    tail -f $FOUNDATIONS_HOME/logs/scheduler.log"
echo "    tail -f $FOUNDATIONS_HOME/logs/yarn.log"
echo "    tail -f $FOUNDATIONS_HOME/logs/orbit_rest_api.log"
echo "    tail -f $FOUNDATIONS_HOME/logs/auth_proxy.lo"