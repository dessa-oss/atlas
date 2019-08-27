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
                config_manager['log_level'] = job_config['log_level']

        deployment = deploy(
            job_config.get('project_name', arguments.project_name), 
            job_config.get('entrypoint', arguments.entrypoint), 
            job_config.get('params', arguments.params)
        )
        try:
            stream_job_logs(deployment)
        except KeyboardInterrupt:
            pass