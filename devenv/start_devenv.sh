#!/usr/bin/env bash

SCRIPT_PID=$$
ATLAS_PORT=37722
GUI_PORT=3000
AUTH_PROXY_PORT=5558

export REACT_APP_API_URL="http://127.0.0.1:${ATLAS_PORT}/api/v1/"
export REACT_APP_API_STAGING_URL="http://localhost:${ATLAS_PORT}/api/v2beta/"
export REDIS_URL="redis://127.0.0.1:6379"
export FOUNDATIONS_SCHEDULER_URL="http://127.0.0.1:5000"
 
function check_status_of_process() {
    process_name=$1
    RESULT=$2
    script_pid=$3

    if [ $RESULT -ne 0  ]; then
        echo "Failed to connect to ${process_name}"
        kill -s TERM $script_pid
    fi
}
function wait_for_url() {
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
}

# ***************************************************************************************************************
# Launch Docker Containers

if docker-compose --compatibility up -d ; then
  echo "Containers up."
else
  echo "Containers failed to start"
  exit 1
fi

# ***************************************************************************************************************
# Launch REST API

echo "Running Atlas REST API on port ${ATLAS_PORT}"
python startup_atlas_api.py ${ATLAS_PORT} > .foundations/logs/atlas_rest_api.log 2>&1 &

echo "Waiting for Atlas REST API to start at http://localhost:${ATLAS_PORT}"
wait_for_url "http://localhost:${ATLAS_PORT}/api/v2beta/projects" 10

check_status_of_process "Atlas REST API" $? $SCRIPT_PID

# ***************************************************************************************************************
# Launch Auth Proxy
if [ ! -d "../../foundations-auth-proxy" ]; 
then 
  cd ../..
  git clone https://github.com/dessa-oss/foundations-auth-proxy.git 
  cd foundations-auth-proxy
else
  cd ../../foundations-auth-proxy
fi

python -m auth_proxy -H localhost -p 5558 > ../atlas/devenv/.foundations/logs/auth_proxy.log 2>&1 &
cd ../atlas/devenv

echo "Waiting for Auth Proxy to start at http://localhost:${AUTH_PROXY_PORT}"
wait_for_url "http://localhost:${AUTH_PROXY_PORT}/" 10

check_status_of_process "Auth Proxy" $? $SCRIPT_PID

# ***************************************************************************************************************
# Launch UI

cd ../foundations_ui && \
  echo "Install UIs dependencies" && \
  yarn install --silent 2> >(grep -v warning 1>&2) 
  echo "Starting the UI in development mode with yarn" && \
  yarn start > ${FOUNDATIONS_HOME}/logs/yarn.log 2>&1 &

cd ../devenv
echo "Waiting for Atlas GUI to start at http://localhost:${GUI_PORT}"
wait_for_url "http://localhost:${GUI_PORT}" 80

check_status_of_process "Atlas GUI" $? $SCRIPT_PID

# ***************************************************************************************************************
# Logs
docker-compose logs -f > .foundations/logs/containers.log 2>&1 &
echo "Check log files for status of programs:"
echo "    tail -f $FOUNDATIONS_HOME/logs/yarn.log"
echo "    tail -f $FOUNDATIONS_HOME/logs/atlas_rest_api.log"
echo "    tail -f devenv/.foundations/logs/containers.log"