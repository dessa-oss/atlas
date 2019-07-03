"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.staging.cached_stage_result import *

class Stage(object):
    def __init__(self, function):
        self._function = function

    def __call__(self, *args, **kwargs):
        return foundations_stage(self._function, *args, **kwargs)

def create_stage(function):
    """
    Takes a Python function as argument and returns a callable with the same signature (receiving the same
    arguments) as the input function. The returned callable can be called in the same way as the input
    function but will create a stage in Foundations instead. Wrapping a function as a stage makes it
    possible for Foundations to track calls, inputs and outputs of the function.

    Arguments:
        function {callable} -- Function to wrap.

    Returns:
        stage_generator {callable} -- A callable that when executed returns a stage object.

    Raises:
        - Runtime error if stage created in running job

    Example:
        ```python
        import foundations
        from data_helper import load_data
        from algorithms import train_model

        load_data = foundations.create_stage(load_data)
        train_model = foundations.create_stage(train_model)
        data = load_data()
        model = train_model(data)
        model.run()
        ```
    """

    from foundations import config_manager
    from foundations_contrib.global_state import current_foundations_context

    if current_foundations_context().is_in_running_job() and not config_manager['run_script_environment'].get('enable_stages', False):
        raise RuntimeError('Cannot create stages in a running stageless job - was code written with stages deployed in a stageless job?')

    return Stage(function)

def cache(function):
    def _callback(*args, **kwargs):
        stage = foundations_stage(function, *args, **kwargs)
        return cached_stage_result(stage)
    return _callback