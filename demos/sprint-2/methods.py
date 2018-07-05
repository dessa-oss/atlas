"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


import pandas as pd


def create_data_frame():
    return pd.DataFrame([[index] for index in range(10)])


def scale_data(data, scale):
    scaled_data = data * scale
    return scaled_data, {'sum': scaled_data[0].sum()}
