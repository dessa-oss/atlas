
from os import getcwd, environ, getenv
import subprocess

# separates test runs
from uuid import uuid4

if "TEST_UUID" not in environ:
    environ["TEST_UUID"] = str(uuid4())
    environ["ARCHIVE_ROOT"] = getcwd() + "/tmp/archives_{}/archive".format(
        environ["TEST_UUID"]
    )

TEST_UUID = environ["TEST_UUID"]
ARCHIVE_ROOT = environ["ARCHIVE_ROOT"]

def envsubst_foundations_home():
    if 'LOCAL_DOCKER_SCHEDULER_HOST' in environ and getenv('RUNNING_ON_CI', False):
        template_file_name = f'{getcwd()}/foundations_home/config/submission/scheduler.config.envsubst.yaml'
        output_file_name = f'{getcwd()}/foundations_home/config/submission/scheduler.config.yaml'
        subprocess.run(f'envsubst < {template_file_name} > {output_file_name}', shell=True)
    
    if not getenv('EXECUTION_REDIS_HOST', None):
        environ['EXECUTION_REDIS_HOST'] = 'localhost'
    if not getenv('EXECUTION_REDIS_PORT', None):
        environ['EXECUTION_REDIS_PORT'] = '6379'

    template_file_name = f'{getcwd()}/foundations_home/config/execution/default.config.envsubst.yaml'
    output_file_name = f'{getcwd()}/foundations_home/config/execution/default.config.yaml'
    subprocess.run(f'envsubst < {template_file_name} > {output_file_name}', shell=True)

def set_foundations_home():
    import os
    os.environ["FOUNDATIONS_HOME"] = os.getcwd() + "/foundations_home"
    os.environ["FOUNDATIONS_COMMAND_LINE"] = "True"

# noinspection PyUnresolvedReferences
def config():
    from foundations import config_manager
    from foundations_contrib.global_state import module_manager
    import sys
    import foundations_spec

    from foundations_core_cli.typed_config_listing import TypedConfigListing
    from foundations_internal.config.execution import translate

    TypedConfigListing("execution").update_config_manager_with_config(
        "default", translate
    )

    module_manager.append_module(sys.modules['foundations_spec'])

set_foundations_home()
envsubst_foundations_home()
config()
