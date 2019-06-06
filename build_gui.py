import docker
import os

client = docker.from_env()
build_version = os.environ['build_version']
rest_api, rest_api_logs = client.images.build(path='.', dockerfile='docker/rest_api_Dockerfile', tag='docker.shehanigans.net/foundations-rest-api:{}'.format(build_version))
rest_api.tag('docker.shehanigans.net/foundations-rest-api', tag='latest')
for line in rest_api_logs:
    print(line)
foundations_gui, foundations_gui_logs = client.images.build(path='foundations_ui', dockerfile='gui_Dockerfile', tag='docker.shehanigans.net/foundations-gui:{}'.format(build_version))
foundations_gui.tag('docker.shehanigans.net/foundations-gui', tag='latest')
for line in foundations_gui_logs:
    print(line)