"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def delete(project_name, monitor_name, env='scheduler'):
    cron_scheduler_callback = lambda scheduler, monitor_id: scheduler.delete_job(monitor_id)
    _modify_monitor(project_name, monitor_name, env, cron_scheduler_callback)


def start(job_directory, command, project_name, name, env):
    import yaml
    from os import path, getcwd
    from foundations_contrib.set_job_resources import set_job_resources
    from foundations_contrib.global_state import current_foundations_context, config_manager
    from foundations_local_docker_scheduler_plugin.bundle_deployment import job_bundle, submit_job_bundle
    from foundations_local_docker_scheduler_plugin.cron_job_scheduler import CronJobScheduler
    from foundations_contrib.change_directory import ChangeDirectory
    from foundations_contrib.global_state import log_manager

    logger = log_manager.get_logger(__name__)

    _update_config(env)
    config = config_manager.config()

    scheduler_url = config.get('scheduler_url', 'http://localhost:5000')

    with ChangeDirectory(job_directory):
        try:
            with open('job.config.yaml', 'r') as file:
                job_config = yaml.load(file.read())
        except IOError:
            job_config = {}

    project_name = project_name or job_config.get('project_name') or path.basename(getcwd())
    name = name or job_config.get('monitor_name') or command[0].replace('.', '-')
    monitor_package = f'{project_name}-{name}'

    monitors_list = get_by_project(project_name)

    if f'{project_name}-{name}'in monitors_list:
        raise ValueError('Monitor already exists')

    logger.info('Creating monitor ...')

    bundle = job_bundle(monitor_package)

    job_resource_args = {}

    if 'log_level' in job_config:
        config['log_level'] = job_config['log_level']
    if 'worker' in job_config:
        config['worker_container_overrides'].update(job_config['worker'])
    if 'num_gpus' in job_config:
        job_resource_args['num_gpus'] = job_config.get('num_gpus')

    config['worker_container_overrides']['args'] = command
    if not path.exists(command[0]):
        print(f"Hey, seems like your command '{command[0]}' is not an existing file in your current directory. If you are using Atlas's advanced custom docker image functionality and know what you are doing, you can ignore this message.")

    set_job_resources(**job_resource_args)

    response = submit_job_bundle(bundle)

    if response.status_code != 200:
        raise RuntimeError(f'Unable to submit job bundle. {response.text}')

    logger.info('Job bundle submitted.')

    foundations_context = current_foundations_context()
    foundations_context.pipeline_context().provenance.monitor_name = name
    username = _get_username()
    monitor_job_spec = _get_monitor_job_spec(project_name, name, username, job_config, config, foundations_context)
    monitor_gpu_spec = _get_monitor_gpu_spec(foundations_context)
    monitor_metadata = {'project_name': project_name, 'monitor_name': name, 'username': username}

    CronJobScheduler(scheduler_url).schedule_job(
        monitor_package,
        monitor_job_spec,
        job_config.get('schedule', {}),
        metadata=monitor_metadata,
        gpu_spec=monitor_gpu_spec
    )

    logger.info('Monitor scheduled.')

    bundle.cleanup()


def pause(project_name, monitor_name, env='scheduler'):
    cron_scheduler_callback = lambda scheduler, monitor_id: scheduler.pause_job(monitor_id)
    _modify_monitor(project_name, monitor_name, env, cron_scheduler_callback)
    return True


def resume(project_name, monitor_name, env='scheduler'):
    cron_scheduler_callback = lambda scheduler, monitor_id: scheduler.resume_job(monitor_id)
    _modify_monitor(project_name, monitor_name, env, cron_scheduler_callback)
    return True


def get_by_project(project_name, env=None):
    from foundations_contrib.global_state import config_manager
    from foundations_local_docker_scheduler_plugin.cron_job_scheduler import CronJobScheduler

    env = env if env is not None else 'scheduler'

    _update_config(env)
    cron_job_scheduler = CronJobScheduler(config_manager.config()['scheduler_url'])
    return cron_job_scheduler.get_job_with_params({'project': project_name})


def _modify_monitor(project_name, monitor_name, env, cron_scheduler_callback):
    from foundations_contrib.global_state import config_manager
    from foundations_local_docker_scheduler_plugin.cron_job_scheduler import CronJobScheduler

    _update_config(env)
    monitor_id = f'{project_name}-{monitor_name}'

    cron_job_scheduler = CronJobScheduler(config_manager.config()['scheduler_url'])
    return cron_scheduler_callback(cron_job_scheduler, monitor_id)


def _update_config(env):
    from foundations_contrib.cli.job_submission.config import load
    load(env)


def _get_username():
    import os
    from getpass import getuser

    username = os.getenv("FOUNDATIONS_USER", None)
    if username is None:
        try:
            username = getuser()
        except KeyError:
            username = 'default'
    return username


def _get_volume_mounts_for_spec(config, project_name, monitor_name):
    from sys import platform
    from pathlib import PurePosixPath, Path

    if platform == 'win32':
        working_dir_root_path = PurePosixPath(config['working_dir_root'])
    else:
        working_dir_root_path = Path(config['working_dir_root']).absolute()

    job_mount_path = str(working_dir_root_path / f'{project_name}-{monitor_name}')
    job_results_root_path = config['job_results_root']
    container_config_root_path = config['container_config_root']
    working_dir_root_path = str(working_dir_root_path)

    return working_dir_root_path, job_mount_path, job_results_root_path, container_config_root_path


def _get_monitor_gpu_spec(foundations_context):
    resources = foundations_context.job_resources()
    gpu_spec = {
        "num_gpus": resources.num_gpus
    }
    return gpu_spec


def _get_monitor_job_spec(project_name, monitor_name, username, job_config, config, foundations_context):
    working_dir_root_path, job_mount_path, job_results_root_path, container_config_root_path = _get_volume_mounts_for_spec(config, project_name, monitor_name)
    import time

    _orbit_spec = {
        'volumes':
                {
                job_mount_path:
                    {
                        "bind": "/job",
                        "mode": "rw"
                    },
                job_results_root_path:
                    {
                        "bind": job_results_root_path,
                        "mode": "rw"
                    },
                container_config_root_path:
                    {
                        "bind": "/root/.foundations/config",
                        "mode": "rw"
                    },
                working_dir_root_path:
                    {
                        "bind": working_dir_root_path,
                        "mode": "rw"
                    }
                },
            "working_dir": "/job/job_source",
            'environment':
                {
                    "FOUNDATIONS_USER": username,
                    "PROJECT_NAME": project_name,
                    "MONITOR_NAME": monitor_name,
                    "FOUNDATIONS_JOB_ID": f'{project_name}-{monitor_name}',
                    "PYTHONPATH": "/job/",
                    "FOUNDATIONS_HOME": "/root/.foundations/",
                    "TZ": time.tzname[0]
                },
            "network": "foundations-orbit"
    }

    worker_container_overrides = config.get('worker_container_overrides')

    if (foundations_context.job_resources().num_gpus is not None
            and foundations_context.job_resources().num_gpus > 0):
        _orbit_spec['image'] = 'orbit/worker-gpu:latest'
        _orbit_spec['runtime'] = 'nvidia'

    else:
        _orbit_spec['image'] = 'docker.shehanigans.net/orbit-team-dev/worker:latest'
        _orbit_spec['runtime'] = 'runc'

    for override_key in ['image', 'working_dir', 'entrypoint']:
        if override_key in worker_container_overrides: 
            _orbit_spec[override_key] = worker_container_overrides[override_key]

    for override_key in ['environment', 'volumes']:
        if override_key in worker_container_overrides:
            _orbit_spec[override_key] = {**_orbit_spec[override_key], **worker_container_overrides[override_key]}

    if 'args' in worker_container_overrides:
            _orbit_spec['command'] = worker_container_overrides['args']

    return _orbit_spec
