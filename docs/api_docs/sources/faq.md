# FAQ

### 1. Docker credentials error during installation on OSX/Windows
The Atlas installer pulls docker images from Google Container Registry during installation.
This can cause the following error on some OSX & Windows systems depending on your docker setup:
`docker.credentials.error.InitializationError: docker-credential-desktop not installed or not available in PATH`

A workaround for this error is:
 - Stop Atlas Server using `atlas-server stop`
 - Restart docker
 - Remove the value of the  `credsStore` tag in your `~/.docker/config.json` so that it looks like `{credsStore: ""}`
 - Start Atlas Server


### 2. Docker Engine Timeout
The Docker Engine can timeout at times if multiple quick running jobs are being run or during download of an image with the following error:
`UnixHTTPConnectionPool(host='localhost', port=None): Read timed out. (read timeout=60)`

This can be addressed by increasing the CPU and RAM allocation to the Docker Engine by navigating to the `Advanced` section in Docker settings/preferences depending on your OS.

### 3. Working directories aren't cleared in Windows

Folder's inside `~/.foundations/local_docker_scheduler/work_dir` do not get cleared out on Windows systems. Folders inside this directory are safe to delete manually once jobs have completed running.


 



