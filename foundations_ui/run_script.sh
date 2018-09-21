#!/bin/bash


function trap_ctrlc ()
{
    # perform cleanup here
    echo "Ctrl-C caught...performing clean up"

    echo "Doing cleanup"
    kill $API_PID
    echo 'API killed'

    exit 2
}

# initialise trap to call trap_ctrlc function when signal 2 (SIGINT) is received
trap "trap_ctrlc" 2

#npm install

python run_api_server.py &
API_PID=$!
echo 'api server started'

yarn start

