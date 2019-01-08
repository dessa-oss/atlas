"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def create_stage(function):
    """
    Transforms any Python function into a callable that represents a stage in Foundations.

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
