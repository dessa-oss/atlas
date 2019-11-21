#!/bin/bash

kill -9 $(lsof -i:37222 -t)
kill -9 $(lsof -i:37722 -t)
kill -9 $(lsof -i:5000 -t)
