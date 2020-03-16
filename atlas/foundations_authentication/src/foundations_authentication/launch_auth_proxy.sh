#!/bin/bash


docker run -d --rm --name auth-proxy \
    -p 8080:8080 \
    us.gcr.io/atlas/auth-proxy:latest