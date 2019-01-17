#!/bin/bash

export REACT_APP_API_URL=/foundations_rest_api/api/v1/
export REACT_APP_BETA_API_URL=/foundations_rest_api/api/v2beta/

envsubst '$SERVER_NAME$FOUNDATIONS_REST_API' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && \
    nginx -g 'daemon off;'