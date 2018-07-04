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

def impute_for_one_hot(data_frame, column, allowed_values, value):
    data_frame.loc[~data_frame[column].isin(allowed_values), column] = value
    return data_frame

def one_hot_encode(data_frame, column):
    encoding = pd.get_dummies(data_frame[column], prefix=column)
    for new_column in encoding:
        assign_columns(data_frame, new_column, encoding[new_column])
    return data_frame

def get_mode(data_frame, column):
    data_frame_without_nans = data_frame.dropna(subset=[column])
    return data_frame_without_nans[column].value_counts().idxmax()

def encode(data_frame, encoder, columns):
    results = encoder.transform(data_frame[columns])
    if isinstance(results, pd.DataFrame):
        for column in results:
            assign_columns(data_frame, column, results[column])
    else:
        assign_columns(data_frame, columns, results)
    return data_frame

def assign_columns(data_frame, columns, value):
    data_frame[columns] = value
    return data_frame

def union(first, second):
    return pd.concat([first, second])

def require(data, *args):
    return data