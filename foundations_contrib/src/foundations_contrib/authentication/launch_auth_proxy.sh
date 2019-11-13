#!/bin/bash


docker run -d --rm --name auth-proxy \
    -p 8080:8080 \
    docker.shehanigans.net/auth-proxy:latest