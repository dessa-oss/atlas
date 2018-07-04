"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat import config_manager, LocalFileSystemCacheBackend
from uuid import uuid4

config_manager['cache_implementation'] = {
    'cache_type': LocalFileSystemCacheBackend,
    'constructor_arguments': ['/tmp/vcat_example_' + str(uuid4())],
}
