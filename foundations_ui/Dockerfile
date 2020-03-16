
FROM node:10.16-alpine

RUN apk add --no-cache gettext libintl nginx openssl && \
    mkdir /run/nginx/ && \
    nginx && \ 
    openssl req -x509 -nodes -days 365 \
                -subj "/C=CA/ST=Ontario/L=Toronto/O=Dessa/OU=Engineering/CN=localhost" \
                -newkey rsa:2048 \
                -keyout /etc/nginx/localhost.key \
                -out /etc/nginx/localhost.crt

COPY --from=loicmahieu/alpine-envsubst /usr/local/bin/envsubst /usr/local/bin/envsubst

RUN mkdir -p /var/foundations_ui
WORKDIR /var/foundations_ui

ENV REACT_APP_API_URL=/foundations_rest_api/api/v1/
ENV REACT_APP_API_STAGING_URL=/foundations_rest_api/api/v2beta/
ENV REACT_APP_SCHEDULER_TYPE=CE
ENV SERVER_NAME=localhost
ENV NODE_OPTIONS=--max_old_space_size=8192

COPY ./ /var/foundations_ui/

RUN npm install -g -s --no-progress yarn && \
    yarn && \
    yarn run build && \
    yarn run prune && \
    yarn cache clean

EXPOSE 8011
COPY deploy/nginx.conf /etc/nginx/nginx.conf.template
CMD ["/bin/sh", "/var/foundations_ui/deploy/run_ui.sh"]
