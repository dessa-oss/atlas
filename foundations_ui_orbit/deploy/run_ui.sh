#!/bin/bash

export REACT_APP_API_URL="http://localhost:37722/api/v1/"
export REACT_APP_APIARY_URL="http://private-d03986-iannelladessa.apiary-mock.com/api/v1/";

envsubst '$SERVER_NAME$FOUNDATIONS_REST_API' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && \
    nginx -g 'daemon off;'