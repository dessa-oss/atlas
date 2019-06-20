"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.global_state import foundations_context
from foundations.staging.cached_stage_result import *

class Stage(object):
    def __init__(self, function):
        self._function = function

    def __call__(self, *args, **kwargs):
        return foundations_context.pipeline().stage(self._function, *args, **kwargs)

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
        - This function doesn't raise exceptions

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

    return Stage(function)
