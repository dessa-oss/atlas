"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
This file contains code commonly used during data preparation / data cleaning.
In the Foundations framework, code is expected to be structured into stages - instead
of a monolithic code block, you have functions which represent stages in a job.

Something very important to note: there is no usage of the Foundations library itself
in this file.  The main thing that you need to do is simply structure your code
as composable functions.

See models.py in this directory for a note on what the signature of stage function should
look like.
"""

import pandas as pd
from sklearn.preprocessing import Imputer
from common.encoder_wrapper import EncoderWrapper
from common.one_hot_encoder import OneHotEncoder


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


def train_imputer(data_frame, numeric_columns, *imputer_args, **imputer_kwargs):

    encoder = Imputer(*imputer_args, **imputer_kwargs)
    encoder = EncoderWrapper(encoder, numeric_columns)
    encoder = encoder.fit(data_frame)

    return encoder


def train_one_hot_encoder(data_frame, categorical_columns):
    encoder = OneHotEncoder()
    encoder = EncoderWrapper(encoder, categorical_columns)
    encoder = encoder.fit(data_frame)

    return encoder


def drop_non_numeric(data_frame):
    return data_frame.select_dtypes(['number'])
