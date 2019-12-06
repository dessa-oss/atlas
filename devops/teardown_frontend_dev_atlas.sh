#!/bin/bash

echo "Attempting to kill proccess for Orbit REST API"
kill -9 $(lsof -i:37222 -t) >/dev/null 2>&1
echo "Attempting to kill proccess for Atlas REST API"
kill -9 $(lsof -i:37722 -t) >/dev/null 2>&1
echo "Attempting to kill proccess for the local docker scheduler"
kill -9 $(lsof -i:5000 -t) >/dev/null 2>&1
echo "Attempting to kill proccess for the UI"
kill -9 $(lsof -i:3000 -t) >/dev/null 2>&1
echo "Attempting to kill proccess for the Auth Proxy"
kill -9 $(lsof -i:5558 -t) >/dev/null 2>&1
