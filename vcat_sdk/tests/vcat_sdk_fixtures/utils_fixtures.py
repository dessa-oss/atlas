"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def create_generator():
    for num in range(10):
        yield num

def create_effectful_generator():
    for num in range(10):
        if num == 0:
            yield num
        else:
            raise Exception("side_effect")

def create_empty_generator():
    for num in range(0):
        yield num