FROM node:10.16.3-alpine

ENV HTTP_SERVER_VERSION 0.9.0
ENV PUBLIC_FOLDER /opt/www

RUN mkdir -p $PUBLIC_FOLDER

RUN npm config set unsafe-perm true && \
    npm install -g http-server@0.11.1 && \
    npm config set unsafe-perm false

CMD http-server $PUBLIC_FOLDER

EXPOSE 8080