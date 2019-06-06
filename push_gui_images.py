import docker 
import os

client = docker.from_env()
build_version = os.environ['build_version']
nexus_password = os.environ['NEXUS_PASSWORD']
nexus_username = os.environ['NEXUS_USER']
nexus_registry = os.environ['NEXUS_DOCKER_REGISTRY']

client.login(username=nexus_username, password=nexus_password, registry=nexus_registry)

try:
    push_logs = client.images.push(repository=nexus_registry + '/' + 'foundations-rest-api', tag=build_version)
finally:
    print(push_logs)
try:
    push_logs = client.images.push(repository=nexus_registry + '/' + 'foundations-rest-api', tag='latest')
finally:
    print(push_logs)

try:
    push_logs = client.images.push(repository=nexus_registry + '/' + 'foundations-gui', tag=build_version)
finally:
    print(push_logs)
try:
    push_logs = client.images.push(repository=nexus_registry + '/' + 'foundations-gui', tag='latest')
finally:
    print(push_logs)
