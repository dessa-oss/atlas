"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

# separates test runs
from uuid import uuid4
from os import getcwd, environ

if 'TEST_UUID' not in environ:
    environ['TEST_UUID'] = str(uuid4())
    environ['ARCHIVE_ROOT'] = getcwd(
    ) + '/tmp/archives_{}/archive'.format(environ['TEST_UUID'])

TEST_UUID = environ['TEST_UUID']
ARCHIVE_ROOT = environ['ARCHIVE_ROOT']

def set_foundations_home():
    import os

    os.environ['FOUNDATIONS_HOME'] = os.getcwd() + '/foundations_home'
    os.environ['FOUNDATIONS_COMMAND_LINE'] = 'True'

def config():
    from foundations import config_manager, LocalFileSystemPipelineArchive, LocalFileSystemPipelineListing, LocalFileSystemCacheBackend
    from foundations_contrib.global_state import module_manager
    import foundations_spec
    import sys

    from foundations_core_cli.typed_config_listing import TypedConfigListing
    from foundations_internal.config.execution import translate

    TypedConfigListing('execution').update_config_manager_with_config('default', translate)

    module_manager.append_module(sys.modules['foundations_spec'])


set_foundations_home()
config()
