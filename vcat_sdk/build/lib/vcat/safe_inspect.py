"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.context_aware import ContextAware
import inspect

def getsource(func):
    if isinstance(func, ContextAware):
        return inspect.getsource(func._function)
    else:
        return inspect.getsource(func)

def getsourcefile(func):
    if isinstance(func, ContextAware):
        return inspect.getsourcefile(func._function)
    else:
        return inspect.getsourcefile(func)

def getsourcelines(func):
    if isinstance(func, ContextAware):
        return inspect.getsourcelines(func._function)
    else:
        return inspect.getsourcelines(func)
