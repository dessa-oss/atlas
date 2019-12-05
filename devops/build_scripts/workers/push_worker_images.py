# Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
# Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Susan Davis <s.davis@dessa.com>, 12 2019

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