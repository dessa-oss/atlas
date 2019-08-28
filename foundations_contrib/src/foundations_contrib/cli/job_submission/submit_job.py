"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def submit(arguments):
    from foundations_contrib.cli.job_submission.config import load
    from foundations_contrib.cli.job_submission.deployment import deploy
    from foundations_contrib.cli.job_submission.logs import stream_job_logs
    from foundations_contrib.change_directory import ChangeDirectory
    from foundations_contrib.global_state import config_manager
    from foundations_contrib.set_job_resources import set_job_resources
    import os
    import os.path
    import yaml

    current_directory = os.getcwd()
    with ChangeDirectory(arguments.job_dir or current_directory):
        load(arguments.scheduler_config or 'scheduler')

        job_config = {}
        if os.path.exists('job.config.yaml'):
            with open('job.config.yaml') as file:
                job_config = yaml.load(file.read())

        job_resource_args = {}

        config_manager['worker_container_overrides'] = {}
        if 'log_level' in job_config:
            config_manager['log_level'] = job_config['log_level']
        if 'worker' in job_config:
            config_manager['worker_container_overrides'].update(job_config['worker'])
        if 'num_gpus' in job_config:
            job_resource_args['num_gpus'] = job_config['num_gpus']
        if 'ram' in job_config:
            job_resource_args['ram'] = job_config['ram']

        if arguments.command is not None:
            config_manager['worker_container_overrides']['args'] = arguments.command.split()

        if arguments.num_gpus is not None:
            job_resource_args['num_gpus'] = arguments.num_gpus
        if arguments.ram is not None:
            job_resource_args['ram'] = arguments.ram
        set_job_resources(**job_resource_args)

        deployment = deploy(
            arguments.project_name or job_config.get('project_name'), 
            arguments.entrypoint or job_config.get('entrypoint'), 
            arguments.params or job_config.get('params')
        )
        if arguments.stream_job_logs:
            try:
                stream_job_logs(deployment)
            except KeyboardInterrupt:
                pass
        return deployment