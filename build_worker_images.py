import docker
import os
import foundations


build_version = os.environ['build_version']

def print_logs(logs):
    for line in logs:
        if 'stream' in line:
            print(line['stream'].strip())

worker_file_path='./docker/worker_images/'
dockerfile = 'worker_Dockerfile' 

client = docker.from_env()

worker_tags = ['orbit/worker', 'atlas-ce/worker']
for worker_tag in worker_tags:
    image, image_logs = client.images.build(path=worker_file_path, dockerfile=dockerfile, tag=worker_tag, buildargs=None)
    image.tag(worker_tag, tag='latest')
    print_logs(image_logs)

