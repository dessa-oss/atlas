#!/bin/bash

CWD=`pwd`

export F9S_ENV_TYPE=${F9S_ENV_TYPE:-atlas}

export ATLAS_PORT=${ATLAS_PORT:-37722}
export GUI_PORT=3000

export SCHEDULER_PORT=${SCHEDULER_PORT:-5000}
export SCHEDULER_HOST=${SCHEDULER_HOST:-localhost}
export FOUNDATIONS_SCHEDULER_HOST=$SCHEDULER_HOST
export FOUNDATIONS_SCHEDULER_URL=http://${SCHEDULER_HOST}:${SCHEDULER_PORT}

export REDIS_HOST=${REDIS_HOST:-localhost}
export REDIS_PORT=${REDIS_PORT:-5556}
export REDIS_URL="redis://$REDIS_HOST:$REDIS_PORT"

export TRACKER_NAME=${TRACKER_NAME:-"foundations-tracker"}
export TRACKER_URI="redis://$TRACKER_NAME:$REDIS_PORT"


export AUTH_PROXY_PORT=${AUTH_PROXY_PORT:-5558}
export AUTH_PROXY_HOST=${AUTH_PROXY_HOST:-localhost}
export AUTH_PROXY_URL=http://${AUTH_PROXY_HOST}:${AUTH_PROXY_PORT}
export AUTH_SERVER_URL=http://localhost:8080
export AUTH_CLIENT_CONFIG_PATH=$CWD/atlas/foundations_rest_api/src/foundations_rest_api/config/auth_client_config.yaml

export F9S_LOG_DIR=$FOUNDATIONS_HOME/logs
mkdir -p $F9S_LOG_DIR

export ARCHIVE_DIR=$FOUNDATIONS_HOME/job_data
mkdir -p $ARCHIVE_DIR

export WORKING_DIR=$FOUNDATIONS_HOME/local_docker_scheduler/work_dir
mkdir -p $WORKING_DIR

export JOB_BUNDLE_STORE_DIR=$FOUNDATIONS_HOME/job_bundle_store_dir
mkdir -p $JOB_BUNDLE_STORE_DIR

export NUM_WORKERS=1
export LOCAL_DOCKER_SCHEDULER_DIR=../local-docker-scheduler

export LOCAL_DOCKER_SCHEDULER_HOST=${LOCAL_DOCKER_SCHEDULER_HOST:-localhost}
export REMOTE_FOUNDATIONS_HOME=${REMOTE_FOUNDATIONS_HOME:-$FOUNDATIONS_HOME}

# ***************************************************************************************************************

# CYPRESS Environment Variables

UI_FOLDER="foundations_ui"
FIXTURE_FOLDER="atlas_scheduler"

export CYPRESS_LOCAL_FOUNDATIONS_HOME="${CWD}/${UI_FOLDER}/cypress/fixtures/${FIXTURE_FOLDER}/.foundations" \
export CYPRESS_SCHEDULER_IP="localhost"
export CYPRESS_SCHEDULER_FOUNDATIONS_HOME=$FOUNDATIONS_HOME 
export CYPRESS_SCHEDULER_REDIS_PORT=$REDIS_PORT 
export CYPRESS_GUI_HOST="localhost"
export CYPRESS_GUI_PORT=$GUI_PORT 

# ***************************************************************************************************************

function start_scheduler() {
    echo "Attempting to run scheduler with foundations home set to $FOUNDATIONS_HOME"
    echo "Generating database.config.yaml at $FOUNDATIONS_HOME/config/local_docker_scheduler/" \
        && mkdir -p $FOUNDATIONS_HOME/config/local_docker_scheduler \
        && cat ./devops/envsubsts/database.config.envsubst.yaml | envsubst > $FOUNDATIONS_HOME/config/local_docker_scheduler/database.config.yaml \
        && echo '' \
        && echo "Creating a symbolic link for the scheduler to run locally between $FOUNDATIONS_HOME/config/local_docker_scheduler/database.config.yaml -> $LOCAL_DOCKER_SCHEDULER_DIR/database.config.yaml" \
        && echo '' \
        && rm -f $LOCAL_DOCKER_SCHEDULER_DIR/database.config.yaml \
        && ln -s $FOUNDATIONS_HOME/config/local_docker_scheduler/database.config.yaml $LOCAL_DOCKER_SCHEDULER_DIR/database.config.yaml \
        && echo "Generating tracker.config.yaml at $FOUNDATIONS_HOME/config/local_docker_scheduler/" \
        && cat ./devops/envsubsts/tracker_client_plugins.envsubst.yaml | envsubst > $FOUNDATIONS_HOME/config/local_docker_scheduler/tracker_client_plugins.yaml \
        && echo '' \
        && echo "Creating a symbolic link for the scheduler to run locally between $FOUNDATIONS_HOME/config/local_docker_scheduler/tracker_client_plugins.yaml -> $LOCAL_DOCKER_SCHEDULER_DIR/tracker_client_plugins.yaml" \
        && echo '' \
        && rm -f $LOCAL_DOCKER_SCHEDULER_DIR/tracker_client_plugins.yaml \
        && ln -s $FOUNDATIONS_HOME/config/local_docker_scheduler/tracker_client_plugins.yaml $LOCAL_DOCKER_SCHEDULER_DIR/tracker_client_plugins.yaml \
        && cd $LOCAL_DOCKER_SCHEDULER_DIR \
        && pip install -r requirements_dev.txt > $F9S_LOG_DIR/install.log 2>&1 \
        && python -m local_docker_scheduler -d -p ${SCHEDULER_PORT} > $FOUNDATIONS_HOME/logs/scheduler.log 2>&1 &
    
    # TODO - Need a better check if the scheduler is running (maybe check the port)
    if [ $? == 0 ]; then
        echo "Successfully started the scheduler"
    else
        echo "Unable to start scheduler"
        exit 1
    fi
}

function start_auth_proxy () {
    TYPE=$1
    echo "Attempting to start the auth proxy at port ${AUTH_PROXY_PORT}"
    cd ../foundations-auth-proxy \
        && pip install -r requirements.txt > $F9S_LOG_DIR/install.log 2>&1 \
        && pip install -e . > $F9S_LOG_DIR/install.log 2>&1 \
        && python -m auth_proxy -t $TYPE -p $AUTH_PROXY_PORT --dev > $FOUNDATIONS_HOME/logs/auth_proxy.log 2>&1 &
    
    # TODO - Need a better check if the auth is running (maybe check the port)
    if [ $? == 0 ]; then
        echo "Successfully started the auth proxy"
    else
        echo "Unable to start auth proxy"
        exit 1
    fi
}

function start_auth_server() {
    TYPE=$1
    network_name=foundations-$TYPE
    export AUTH_SERVER_NAME=foundations-authentication-server \
        && echo "Attempting to start the auth server as ${AUTH_SERVER_NAME}" \
        && ./atlas/foundations_authentication/src/foundations_authentication/launch.sh \
        && echo "Connecting the auth server ${AUTH_SERVER_NAME} to network ${network_name}" \
        && docker network connect $network_name $AUTH_SERVER_NAME
}

function check_status_of_process() {
    process_name=$1
    RESULT=$2
    script_pid=$3

    if [ $RESULT -ne 0  ]; then
        echo "Failed to connect to ${process_name}"
        kill -s TERM $script_pid
    fi
}

function check_for_config_and_create_if_does_not_exists() {
    FILE_TYPE=$1
    if [ $FILE_TYPE == "execution" ]; then
        CONFIG_PATH="${FOUNDATIONS_HOME}/config/execution"
        FILE_PATH="${CONFIG_PATH}/default.config.yaml"
        ENVSUBST_FILE="${CWD}/devops/envsubsts/default.config.envsubst.yaml"
    elif [ $FILE_TYPE == "submission" ]; then
        CONFIG_PATH="${FOUNDATIONS_HOME}/config/submission"
        FILE_PATH="${CONFIG_PATH}/scheduler.config.yaml"
        ENVSUBST_FILE="${CWD}/devops/envsubsts/scheduler.config.envsubst.yaml"
    elif [ $FILE_TYPE == "worker_execution" ]; then
        CONFIG_PATH="${FOUNDATIONS_HOME}/config/local_docker_scheduler/worker_config/execution"
        FILE_PATH="${CONFIG_PATH}/default.config.yaml"
        ENVSUBST_FILE="${CWD}/devops/envsubsts/worker.default.config.envsubst.yaml"
    elif [ $FILE_TYPE == "worker_submission" ]; then
        CONFIG_PATH="${FOUNDATIONS_HOME}/config/local_docker_scheduler/worker_config/submission"
        FILE_PATH="${CONFIG_PATH}/scheduler.config.yaml"
        ENVSUBST_FILE="${CWD}/devops/envsubsts/worker.scheduler.config.envsubst.yaml"
    else
        echo "${FILE_TYPE} is an unsupported config file type. Choose between execution, submission, worker_execution and worker_submission"
        exit 1
    fi

    if [ ! -f "$FILE_PATH" ]; then
        mkdir -p $CONFIG_PATH   || true 
        envsubst < $ENVSUBST_FILE > $FILE_PATH
        echo "genertated:"
        cat $FILE_PATH
    else
        echo "${FILE_TYPE} configuration found"  
    fi
}
