"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 03 2019
"""

from foundations_spec import *

class DockerTestMixin(object):

    @let
    def docker_client(self):
        import docker
        return docker.from_env()