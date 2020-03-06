
FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8

ARG main_file

ENV SERVER_NAME=localhost
ENV AUTH_SERVER_URL=http://foundations-authentication-server:8080/auth
ENV AUTH_CLIENT_CONFIG_PATH=/configs/auth_client_config.yaml

COPY --from=loicmahieu/alpine-envsubst /usr/local/bin/envsubst /usr/local/bin/envsubst

RUN mkdir -p /var/foundations ~/.ssh
WORKDIR /var/foundations

RUN apk add --update --no-cache alpine-sdk python-dev libressl-dev libffi-dev linux-headers
RUN pip install -U pip setuptools wheel
COPY ./tmp/pip_wheels /var/foundations/

RUN find -iname "foundations_internal-*.whl" | xargs pip install \
    && find -iname "foundations_events-*.whl" | xargs pip install \
    && find -iname "foundations_contrib-*.whl" | xargs pip install \
    && find -iname "foundations_authentication-*.whl" | xargs pip install \
    && find -iname "foundations_local_docker_scheduler_plugin-*.whl" | xargs pip install \
    && find -iname "foundations_core_rest_api_components-*.whl" | xargs pip install \
    && find -iname "foundations_rest_api-*.whl" | xargs pip install \
    && echo "Completed foundations package installation"

WORKDIR /app/
COPY foundations_rest_api/${main_file} /app/main.py
COPY foundations_rest_api/uwsgi.ini /app/uwsgi.ini

RUN mkdir /configs
COPY foundations_rest_api/src/foundations_rest_api/config/ /configs/
