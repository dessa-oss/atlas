
# separates test runs
from uuid import uuid4
TEST_UUID = uuid4()


def set_foundations_home():
    import os
    os.environ['FOUNDATIONS_HOME'] = os.path.abspath(os.environ.get('FOUNDATIONS_HOME', os.getcwd() + '/local_docker_scheduler_acceptance/foundations_home'))
    os.environ['FOUNDATIONS_COMMAND_LINE'] = 'True'


def _flattened_config_walk():
    import os
    import os.path as path

    for dir_name, _, files in os.walk('local_docker_scheduler_acceptance/foundations_home'):
        for file_name in files:
            if file_name.endswith('.envsubst.yaml'):
                yield path.join(dir_name, file_name)


def _load_execution_config():
    from foundations_core_cli.typed_config_listing import TypedConfigListing
    from foundations_internal.config.execution import translate
    TypedConfigListing('execution').update_config_manager_with_config('default', translate)


def _config():
    import os
    import subprocess

    scheduler_host = os.environ.get('LOCAL_DOCKER_SCHEDULER_HOST')
    redis_host = os.environ.get('REDIS_HOST')
    redis_port = os.environ.get('REDIS_PORT')

    if not scheduler_host:
        print('LOCAL_DOCKER_SCHEDULER_HOST not set')
        exit(1)

    if not redis_host:
        print('REDIS_HOST not set')
        exit(1)

    if not redis_port:
        print('REDIS_PORT not set')
        exit(1)

    for template_file_name in _flattened_config_walk():
        output_file_name = template_file_name[:-len('.envsubst.yaml')] + '.yaml'
        subprocess.run(f'envsubst < {template_file_name} > {output_file_name}', shell=True)

    _load_execution_config()


set_foundations_home()
_config()
