#!/bin/bash

cd vcat_sdk/ && ./build.sh && cd ../ && pip install -U vcat_sdk/dist/vcat-0.0.1-py2-none-any.whl
