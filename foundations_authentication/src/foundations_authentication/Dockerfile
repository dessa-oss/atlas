#
# Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
# Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Cole Clifford <c.clifford@dessa.com>, 11 2019
#

FROM jboss/keycloak

ENV KEYCLOAK_USER admin
ENV KEYCLOAK_PASSWORD admin 
ENV KEYCLOAK_IMPORT /keycloak/atlas.json
ENV KEYCLOAK_LOGLEVEL DEBUG

VOLUME keycloak:/keycloak

EXPOSE 8080
