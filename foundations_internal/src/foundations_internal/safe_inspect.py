"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.context_aware import ContextAware
import inspect

from foundations import log_manager

def getsource(function):
    function = _get_function(function)
    return _log_if_cannot_get_source_code(inspect.getsource, function)

def getsourcefile(function):
    function = _get_function(function)
    return _log_if_cannot_get_source_code(inspect.getsourcefile, function)

def getsourcelines(function):
    function = _get_function(function)
    return _log_if_cannot_get_source_code(inspect.getsourcelines, function)

def _log_if_cannot_get_source_code(action, function):
    try:
        if type(function) == type(len):
            return _fail_gracefully(function)

        return action(function)
    except OSError as e:
        return _fail_gracefully(function)
    except IOError as e:
        return _fail_gracefully(function)

def _get_function(function):
    if isinstance(function, ContextAware):
        function = function.function()

    return function

def _fail_gracefully(function):
    import uuid

    logger = log_manager.get_logger(__name__)
    logger.warning("could not get source code for {}".format(function.__name__))
    return "<could not get source code ({})>".format(str(uuid.uuid4()))