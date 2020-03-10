#!/usr/bin/env bash

docker-compose down --remove-orphans

echo "Attempting to kill proccess for Atlas REST API"
kill -9 $(lsof -i:37722 -t) > /dev/null 2>&1 || true

echo "Attempting to kill proccess for the UI"
kill -9 $(lsof -i:3000 -t) > /dev/null 2>&1 || true