"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import random


def bundle_value(value):
    return value

def add(a, b):
    return a + b

def _make_generator(value):
    yield value

def returns_generator(value):
    return _make_generator(value)

def executes_generator(gen):
    return next(gen)