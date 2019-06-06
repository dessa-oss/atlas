import docker
import os

client = docker.from_env()
build_version = os.environ['build_version']

def build_and_tag_gui_image(path, dockerfile, repository):
    try:
        image, image_logs = client.images.build(path=path, dockerfile=dockerfile, tag='{}:{}'.format(repository, build_version))
        image.tag(repository, tag='latest')
    finally:
        for line in image_logs:
            print(line)

build_and_tag_gui_image('.', 'docker/rest_api_Dockerfile', 'docker.shehanigans.net/foundations-rest-api')
build_and_tag_gui_image('foundations_ui', 'gui_Dockerfile', 'docker.shehanigans.net/foundations-gui')