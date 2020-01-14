#!/bin/bash

export FOUNDATIONS_HOME=${FOUNDATIONS_HOME:-~/.foundations}

export ATLAS_PORT=${ATLAS_PORT:-37722}
export ORBIT_PORT=${ORBIT_PORT:-37222}

export SCHEDULER_PORT=${SCHEDULER_PORT:-5000}
export SCHEDULER_HOST=${SCHEDULER_HOST:-localhost}
export FOUNDATIONS_SCHEDULER_URL=http://${SCHEDULER_HOST}:${SCHEDULER_PORT}

export REDIS_HOST=${REDIS_HOST:-localhost}
export REDIS_PORT=${REDIS_PORT:-6379}
export REDIS_URL="redis://$REDIS_HOST:$REDIS_PORT"

export AUTH_PROXY_PORT=5558

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
        && pip install -r requirements_dev.txt \
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
    echo "Attempting to start the auth proxy at port ${AUTH_PROXY_PORT}"
    cd ../foundations-auth-proxy \
        && pip install -r requirements.txt \
        && pip install -e . \
        && python -m auth_proxy -p $AUTH_PROXY_PORT --dev > $FOUNDATIONS_HOME/logs/auth_proxy.log 2>&1 &
    
    # TODO - Need a better check if the auth is running (maybe check the port)
    if [ $? == 0 ]; then
        echo "Successfully started the auth proxy"
    else
        echo "Unable to start auth proxy"
        exit 1
    fi
}

function start_auth_proxy_orbit () {
    echo "Attempting to start the auth proxy at port ${AUTH_PROXY_PORT}"
    cd ../foundations-auth-proxy \
        && pip install -r requirements.txt \
        && pip install -e . \
        && python -m auth_proxy -t orbit -p $AUTH_PROXY_PORT --dev > $FOUNDATIONS_HOME/logs/auth_proxy.log 2>&1 &
    
    # TODO - Need a better check if the auth is running (maybe check the port)
    if [ $? == 0 ]; then
        echo "Successfully started the auth proxy"
    else
        echo "Unable to start auth proxy"
        exit 1
    fi
}

function start_auth_server() {
    export AUTH_SERVER_NAME=foundations-authentication-server \
        && echo "Attempting to start the auth server as ${AUTH_SERVER_NAME}" \
        && ./foundations_contrib/src/foundations_contrib/authentication/launch.sh \
        && echo "Connecting the auth server ${AUTH_SERVER_NAME} to network ${network_name}" \
        && docker network connect $network_name $AUTH_SERVER_NAME
}