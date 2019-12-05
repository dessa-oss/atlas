export REACT_APP_API_URL="http://private-d03986-iannelladessa.apiary-mock.com/api/v1/"
export REACT_APP_API_STAGING_URL="http://private-d03986-iannelladessa.apiary-mock.com/api/v2beta/"
export REACT_APP_APIARY_URL="http://private-d03986-iannelladessa.apiary-mock.com/api/v1/"
FOUNDATION_DIR="/var/foundations"
if [ ! -d "$FOUNDATION_DIR" ]; then
    echo "Creating Foundation directory at: $FOUNDATION_DIR"
    sudo mkdir $FOUNDATION_DIR
fi
echo "Creating abnd setting permissions for the log file used by the rest api"
sudo touch /var/foundations/rest_api.log
sudo chmod 666 /var/foundations/rest_api.log



run_redis_through_docker () {
    docker run -d -p 6379:6379 -v /tmp/foundations-persis:/data redis
    export REDIS_URL=redis://localhost:6379
}

echo "Running Redis through docker" 
run_redis_through_docker &

