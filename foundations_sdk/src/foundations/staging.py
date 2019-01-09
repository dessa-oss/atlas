"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def create_stage(function):
    """
    Given a Python function, returns a callable with the same signature (receiving the same arguments) as the
    wrapped function which can be called in the same way as the wrapped function but will create a stage
    in Foundations instead.

    Arguments:
        function {callable} -- Function to wrap.

    Returns:
        stage_generator {callable} -- A callable that when executed returns a stage object.

    Raises:
        - This function doesn't raise exceptions.
    """

    def stage(*args, **kwargs):
        from foundations.global_state import foundations_context
        return foundations_context.pipeline().stage(function, *args, **kwargs)
    return stage
