#!/usr/bin/env bash

for file in $(find .foundations -type f -name "*.config"); do \
    envsubst < $file > $file.yaml
done

