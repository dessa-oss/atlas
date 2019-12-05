import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.modules[__name__].__file__), "..")))


if __name__ == '__main__':
    from helpers.docker_utils import push_image_to_repository

    push_image_to_repository(image_name='foundations-rest-api')
    push_image_to_repository(image_name='foundations-gui')