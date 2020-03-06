#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
AUTH_SERVER_NAME=${AUTH_SERVER_NAME:-foundations-authentication-server}


docker run -d --rm --name $AUTH_SERVER_NAME \
    -e KEYCLOAK_USER=admin \
    -e KEYCLOAK_PASSWORD=admin \
    -e KEYCLOAK_IMPORT=/keycloak/atlas.json \
    -e KEYCLOAK_LOGLEVEL=DEBUG \
    -v $DIR/keycloak:/keycloak \
    -p 8080:8080 \
    jboss/keycloak:8.0.1
