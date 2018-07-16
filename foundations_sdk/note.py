"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from foundations import *
from pandas import DataFrame


def create_data_frame():
    return DataFrame([[0]], columns=["hello"])


def print_it(thing):
    print(thing)
    return thing


data_frame = pipeline | create_data_frame
something = data_frame["hello"].count() | print_it
thing = data_frame["world"] = [99999]
print(thing)
something.run()
