"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import pandas as pd


def fillna(data_frame, column, value):
    data_frame[column].fillna(value, inplace=True)
    return data_frame

def one_hot_encode(data_frame, column):
    encoding = pd.get_dummies(data_frame[column], prefix=column)
    for new_column in encoding:
        data_frame[new_column] = encoding[new_column]
    return data_frame

def get_mode(data_frame, column):
    data_frame_without_nans = data_frame.dropna(subset=[column])
    return data_frame_without_nans[column].value_counts().idxmax()