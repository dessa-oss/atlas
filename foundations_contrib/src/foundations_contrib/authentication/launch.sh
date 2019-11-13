#!/usr/bin/env sh

docker run -d --rm --name keycloak \
    -e KEYCLOAK_USER=admin \
    -e KEYCLOAK_PASSWORD=admin \
    -e KEYCLOAK_IMPORT=/keycloak/atlas.json \
    -e KEYCLOAK_LOGLEVEL=DEBUG \
    -v $(realpath keycloak):/keycloak \
    -p 8080:8080 \
    jboss/keycloak