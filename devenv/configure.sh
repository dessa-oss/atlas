#!/usr/bin/env bash

for file in $(find .foundations -type f -name "*.config"); do \
    envsubst < $file > $file.yaml
done

# .docker is missing in github actions runner
if [ ! -d "$HOME/.docker"]; then
    mkdir $HOME/.docker
fi
