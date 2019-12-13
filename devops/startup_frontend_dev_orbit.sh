#!/bin/bash

source activate_dev_env.sh
source ./devops/set_environment_for_docker_scheduler.sh

./devops/teardown_frontend_dev_orbit.sh

echo "Note: Ensure you have redis running and accessible at ${REDIS_URL}"

echo "Running Atlas REST API on port ${ATLAS_PORT}"
python devops/startup_atlas_api.py ${ATLAS_PORT} &

echo "Running Orbit REST API on port ${ORBIT_PORT}"
python devops/startup_orbit_api.py ${ORBIT_PORT} &

echo "Generating database.config.yaml at $FOUNDATIONS/config/local_docker_scheduler/" \
  && cat ./devops/envsubsts/database.config.envsubst.yaml | envsubst > $FOUNDATIONS/config/local_docker_scheduler/database.config.yaml \
  && echo '' \
  && echo 'Creating a symbolic link for the scheduler to run locally between $FOUNDATIONS/config/local_docker_scheduler/database.config.yaml -> $LOCAL_DOCKER_SCHEDULER_DIR/database.config.yaml' \
  && echo '' \
  && rm -f $LOCAL_DOCKER_SCHEDULER_DIR/database.config.yaml \
  && ln -s $FOUNDATIONS/config/local_docker_scheduler/database.config.yaml $LOCAL_DOCKER_SCHEDULER_DIR/database.config.yaml \
  && echo "Generating tracker.config.yaml at $FOUNDATIONS/config/local_docker_scheduler/" \
  && cat ./devops/envsubsts/tracker_client_plugins.envsubst.yaml | envsubst > $FOUNDATIONS/config/local_docker_scheduler/tracker_client_plugins.yaml \
  && echo '' \
  && echo 'Creating a symbolic link for the scheduler to run locally between $FOUNDATIONS/config/local_docker_scheduler/tracker_client_plugins.yaml -> $LOCAL_DOCKER_SCHEDULER_DIR/tracker_client_plugins.yaml' \
  && echo '' \
  && rm -f $LOCAL_DOCKER_SCHEDULER_DIR/tracker_client_plugins.yaml \
  && ln -s $FOUNDATIONS/config/local_docker_scheduler/tracker_client_plugins.yaml $LOCAL_DOCKER_SCHEDULER_DIR/tracker_client_plugins.yaml \
  && cd $LOCAL_DOCKER_SCHEDULER_DIR \
  && pip install -r requirements_dev.txt \
  && python -m local_docker_scheduler -p ${SCHEDULER_PORT} > $FOUNDATIONS/logs/scheduler.log 2>&1 &

cd foundations_ui_orbit && \
  echo "Install UI dependencies" && \
  yarn install && \
  echo "Starting the UI in development mode with yarn" && \
  yarn start > $FOUNDATIONS/logs/yarn.log 2>&1 &

echo "Running UI on port 3000"

echo "Check log files for status of programs:"
echo "    tail -f $FOUNDATIONS/logs/scheduler.log"
echo "    tail -f $FOUNDATIONS/logs/yarn.log"
echo "    tail -f $FOUNDATIONS/logs/orbit_rest_api.log"