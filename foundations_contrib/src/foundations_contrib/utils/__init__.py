"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from contextlib import contextmanager
import subprocess as sp
import os

from foundations_internal.utils import *


def foundations_home():
    import os
    from sys import platform
    from os.path import expanduser

    if platform == 'win32':
        return os.environ.get('FOUNDATIONS_HOME', expanduser(os.path.join('~', '.foundations')))
    else:
        return os.environ.get('FOUNDATIONS_HOME', '~/.foundations')


def force_encoding(string):
    return string.encode('utf-8', 'ignore')


def byte_string(string):
    if isinstance(string, bytes):
        return string
    else:
        return bytes(force_encoding(string))


def string_from_bytes(string):
    if is_string(string):
        return string
    else:
        return string.decode()


def force_encoding(string):
    return string.encode('utf-8', 'ignore')


def byte_string(string):
    if isinstance(string, bytes):
        return string
    else:
        return bytes(force_encoding(string))


def string_from_bytes(string):
    if is_string(string):
        return string
    else:
        return string.decode()


def is_number(number):
    return isinstance(number, (int, float))


def file_archive_name(prefix, name):
    if prefix is not None:
        return prefix + '/' + name
    else:
        return name


def file_archive_name_with_additional_prefix(prefix, additional_prefix, name):
    return file_archive_name(prefix, additional_prefix + '/' + name)


def run_command(command: str, timeout: int=60, **kwargs) -> sp.CompletedProcess:
    fixed_kwargs = { 'shell': True, 'stdout': sp.PIPE, 'stderr': sp.PIPE, 'timeout': timeout, 'check': True}
    kwargs.update(fixed_kwargs)
    try:
        result = sp.run(command, **kwargs)
    except sp.TimeoutExpired as error:
        print('Command timed out.')
        print(error.stdout.decode())
        raise Exception(error.stderr.decode())
    except sp.CalledProcessError as error:
        print(f'Command failed: \n\t{command}\n')
        raise Exception(error.stderr.decode())
    return result

@contextmanager
def cd(path):
    prev_path = os.getcwd()
    os.chdir(os.path.expanduser(path))
    try:
        yield
    finally:
        os.chdir(prev_path)


def save_project_to_redis(project_name):
    from time import time
    from foundations_contrib.global_state import redis_connection

    timestamp = time()
    redis_connection.execute_command('ZADD', 'projects', 'NX', timestamp, project_name)


def is_job_running(pipeline_context):
    try:
        return pipeline_context.file_name is not None
    except ValueError:
        return False
