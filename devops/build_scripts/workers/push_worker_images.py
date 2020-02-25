
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.modules[__name__].__file__), "..")))


if __name__ == '__main__':
    from build_worker_images import  build_worker_tags_for_local_development
    from helpers.docker_utils import push_image_to_repository
    
    workers = build_worker_tags_for_local_development()
    for worker in workers:
        # the push image will add the registry and build version
        push_image_to_repository(worker)