"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.global_state import current_foundations_context
from foundations_internal.job_resources import JobResources

def set_job_resources(num_gpus, ram):
    """
    Specifies the resources to run a job with. The available amount will greatly depend on what is available on the infrastrcture that the Foundations job orchestrator is setup on.

    Arguments:
        num_gpus {int} -- The number of GPUs to run the job with. By default uses 0, indicating the job will run with CPU resources instead.
        ram {number} -- The amount of ram in GB to use while running the job. Must be greater than 0.

    Returns:
        - This function doesn't return a value.

    Raises:
        ValueError -- If either the RAM or GPU quantity is an invalid value (ex: less than 0) or not specified.

    Notes:
        Setting the resources for a job will apply to all future jobs even if the function is not present in the code as it updates the configuration on the orchestrator side. To clear specifying resources and use the default
        or CPU resources, you can pass in set_job_resources(0, None).

    Example:
        ```python
        import foundations
        from algorithms import train_model

        foundations.set_job_resources(1, 1)
        train_model = foundations.create_stage(train_model)
        model = train_model()
        model.run()
        ```
    """
    if ram is not None and ram <= 0:
        raise ValueError('Invalid RAM quantity. Please provide a RAM quantity greater than zero.')
    
    if not isinstance(num_gpus, int) or num_gpus < 0:
        raise ValueError('Invalid GPU quantity. Please provide a non-negative integer GPU quantity.')

    job_resources = JobResources(num_gpus, ram)
    current_foundations_context().set_job_resources(job_resources)
