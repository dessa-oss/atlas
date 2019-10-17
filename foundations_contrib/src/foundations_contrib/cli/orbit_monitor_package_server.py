"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def delete(project_name, monitor_name, env):
    pass


def start(job_directory, command, project_name, name, env):    
    pass
        

def _update_config(env):
    from foundations_contrib.cli.job_submission.config import load

    load(env)

def _get_scheduler_url(env):
    from foundations_contrib.global_state import config_manager

    _update_config(env)
    return config_manager.get('scheduler_url', 'http://localhost:5000')