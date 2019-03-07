"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import foundations
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

def throws_exception(input):
    try:
        raise Exception(str(input))
    except Exception as e:
        return e

def return_error_message(err):
    return "error code: " + str(err)

def get_and_log_python_path_as_metric():
    import sys

    python_path = sys.executable
    foundations.log_metric("python_path", python_path)

def add_two_numbers(num1, num2):
    return num1 + num2
