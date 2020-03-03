# Atlas Server
## Overview

## Requirements:
1. OS is linux or MacOS
2. Docker
3. Foundations SDK

## Installation
1. **Download installer**

    Clone this repo

2. **Configure execution settings**

    Run `./config.sh` to configure your `$FOUNDATIONS_HOME/execution.config.yaml`.  
    Use `-h` or `--help` to see configuration options.

3. (Optional) **Use local scheduler**

    Append the following dictionary to the `spec` list variable inside `AtlasStandalone._container_specs()`:
    
```
  {
      "image": "<scheduler_and_tag>",
      "name": "foundations-local-docker-scheduler",
      "ports": {5000: 5000},
      "volumes": {"</path/to/local/docker_socket>": {'bind': "/var/run/docker.sock", 'mode': 'rw'},
                  "</path/to/local/docker_config>": {'bind': "/root/.docker", 'mode': 'rw'},
                  "</path/to/local/tracker_client_plugins.yaml>": {'bind': "/app/local-docker-scheduler/tracker_client_plugins.yaml", 'mode': 'rw'}}
  }
  
```


    where `docker_socket`, `docker_config`, and `tracker_client_plugins` are strings that point to these objects in the host file system.  
    The first two typically take the default path of `docker_socket=/var/run/docker.sock`, `docker_config=~/.docker`.  
    See the `local-docker-scheduler` repo to see how to configure the `tracker_client_plugins` file.  
    `scheduler_and_tag` is image name of the scheduler image. Consult the `local-docker-scheduler` repo to build this image locally.

## Quick start

Start Atlas server using `python -m atlas-server start`
Use `-h` or `--help` to see optional parameters
