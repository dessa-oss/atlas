"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


import pandas as pd


def create_data_frame():
    return pd.DataFrame([range(10)])


def join_data(left, right):
    return pd.concat([left, right])


def print_it(data):
    print(data)
