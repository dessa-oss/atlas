#!/bin/bash

AUTH_SERVER_NAME=${AUTH_SERVER_NAME:-foundations-authentication-server}

docker rm -f $AUTH_SERVER_NAME || true;