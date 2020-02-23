

from collections import namedtuple

_attribute_list = [
    'scheduler_config',
    'job_directory',
    'project_name',
    'entrypoint',
    'params',
    'ram',
    'num_gpus',
    'stream_job_logs',
    'command',
]
_deployment_arguments = namedtuple('_deployment_arguments', _attribute_list)
_deployment_arguments.__new__.__defaults__ = (None,) * len(_attribute_list)


def submit(**kwargs):
    from foundations_core_cli.job_submission.submit_job import submit
    from foundations_contrib.global_state import push_state, pop_state

    arguments = _deployment_arguments(**kwargs)
    try:
        push_state()
        return submit(arguments)
    finally:
        pop_state()
