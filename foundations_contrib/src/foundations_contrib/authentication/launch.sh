#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker run -d --rm --name keycloak \
    -e KEYCLOAK_USER=admin \
    -e KEYCLOAK_PASSWORD=admin \
    -e KEYCLOAK_IMPORT=/keycloak/atlas.json \
    -e KEYCLOAK_LOGLEVEL=DEBUG \
    -v $DIR/keycloak:/keycloak \
    -p 8080:8080 \
    jboss/keycloak