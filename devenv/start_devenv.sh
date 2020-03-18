#!/usr/bin/env bash

SCRIPT_PID=$$
ATLAS_PORT=37722
GUI_PORT=3000

export TENSORBOARD_API_HOST="http://localhost:5001"
export REACT_APP_API_URL="http://127.0.0.1:${ATLAS_PORT}/api/v1/"
export REACT_APP_API_STAGING_URL="http://localhost:${ATLAS_PORT}/api/v2beta/"
 
function check_status_of_process() {
    process_name=$1
    RESULT=$2
    script_pid=$3

    if [ $RESULT -ne 0  ]; then
        echo "Failed to connect to ${process_name}"
        kill -s TERM $script_pid
    fi
}

# ***************************************************************************************************************
# Launch Docker Containers

docker-compose up -d

# ***************************************************************************************************************
# Launch REST API

echo "Running Atlas REST API on port ${ATLAS_PORT}"
python startup_atlas_api.py ${ATLAS_PORT} > .foundations/logs/atlas_rest_api.log 2>&1 &

echo "Waiting for Atlas REST API to start at http://localhost:${ATLAS_PORT}"
./wait_for_url.sh "http://localhost:${ATLAS_PORT}/api/v2beta/projects" 10

check_status_of_process "Atlas REST API" $? $SCRIPT_PID

# ***************************************************************************************************************
# Launch UI

cd ../foundations_ui && \
  echo "Install UIs dependencies" && \
  yarn install --silent 2> >(grep -v warning 1>&2) 
  echo "Starting the UI in development mode with yarn" && \
  yarn start > ${FOUNDATIONS_HOME}/logs/yarn.log 2>&1 &

cd ../devenv
echo "Waiting for Atlas GUI to start at http://localhost:${GUI_PORT}"
./wait_for_url.sh "http://localhost:${GUI_PORT}" 80

check_status_of_process "Atlas GUI" $? $SCRIPT_PID

# ***************************************************************************************************************
# Logs
docker-compose logs -f > .foundations/logs/containers.log 2>&1 &
echo "Check log files for status of programs:"
echo "    tail -f $FOUNDATIONS_HOME/logs/yarn.log"
echo "    tail -f $FOUNDATIONS_HOME/logs/atlas_rest_api.log"
echo "    tail -f devenv/.foundations/logs/containers.log"