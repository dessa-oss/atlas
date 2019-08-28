"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Foundations Team <pairing@dessa.com>, 06 2018
"""


from collections import namedtuple

_deployment_arguments = namedtuple('_deployment_arguments',
                                   [
                                       'scheduler_config',
                                       'job_dir',
                                       'project_name',
                                       'entrypoint',
                                       'params',
                                       'ram',
                                       'num_gpus',
                                       'stream_job_logs',
                                   ])
_deployment_arguments.__new__.__defaults__ = (None,) * 8


def submit(**kwargs):
    from foundations_contrib.cli.job_submission.submit_job import submit

    arguments = _deployment_arguments(**kwargs)
    return submit(arguments)
