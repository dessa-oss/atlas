
from foundations_contrib.global_state import current_foundations_context
from foundations_internal.job_resources import JobResources

def set_job_resources(num_gpus=0, ram=None):
    """
    Specifies the resources to run a job with. The available amount will greatly depend on what is available on the infrastrcture that the Foundations job orchestrator is setup on.

    Arguments:
        num_gpus {int} -- The number of GPUs to run the job with.  Set to 0 to run with CPU resources instead.  By default uses 1 GPU.
        ram {number} -- The amount of ram in GB to use while running the job. Must be greater than 0 or None.  If None, no limit will be set.

    Returns:
        - This function doesn't return a value.

    Raises:
        ValueError -- If either the RAM or GPU quantity is an invalid value (ex: less than 0) or not specified.

    Notes:
        Setting the resources for a job from a given notebook or driver file will cause any additional jobs (ex: hyperparameter search) deployed from the same file and using the same process to use the same resources, unless specified otherwise.
        To clear specifying resources and use the default, you can pass in set_job_resources(1, None).  Set num_gpus=0 to use CPU instead.
    """
    if ram is not None and ram <= 0:
        raise ValueError('Invalid RAM quantity. Please provide a RAM quantity greater than zero.')
    
    if not isinstance(num_gpus, int) or num_gpus < 0:
        raise ValueError('Invalid GPU quantity. Please provide a non-negative integer GPU quantity.')

    job_resources = JobResources(num_gpus, ram)
    current_foundations_context().job_resources = job_resources
