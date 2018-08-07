"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
This file contains code used in the ETL pipeline for the (in)famous Titanic example.
In the Foundations framework, code is expected to be structured into stages - instead
of a monolithic code block, you have functions which represent stages in a pipeline.

Something very important to note: there is no usage of the Foundations library itself
in this file.  The main thing that you need to do is simply structure your code
as composable functions.

The signature of such a function is as follows:
    - arguments are unrestricted - there can be as many as you want, in any order
    - it should return as its first value the object to pass to the next stage
    - if you want to pass multiple items to the next stage, or return multiple items,
        explicitly return a list (see "split_inputs_and_targets" below)
    - if logging is to be done, the item to be logged (a metric for example) should be 
        stored in a dict with some key, and the dict should be returned as a second
        return value (see "get_metrics" below)
"""

from common.data import load_titanic
from common.prep import fillna, train_imputer, train_one_hot_encoder, drop_non_numeric
from common.models import get_metrics_internal
from sklearn.model_selection import train_test_split


def load_data():
    return load_titanic()


def fill_categorical_nulls(data):
    data = fillna(data, 'Cabin', 'NULLCABIN')
    data = fillna(data, 'Embarked', 'NULLEMBARKED')
    return data


def split_inputs_and_targets(data):
    inputs = data[['Age', 'SibSp', 'Parch', 'Fare',
                   'Pclass', 'Sex', 'Cabin', 'Embarked']]
    targets = data[['Survived']]
    return [inputs, targets]


def split_training_and_validation(inputs, targets):
    return train_test_split(inputs, targets, test_size=0.2, random_state=42, stratify=targets.as_matrix())


def create_imputer(data):
    return train_imputer(data, ['Age', 'Fare'])


def impute(x_train, x_valid):
    encoder = create_imputer(x_train)
    x_train = encoder.transform(x_train)
    x_valid = encoder.transform(x_valid)
    return [x_train, x_valid]


def create_one_hot_encoder(data):
    return train_one_hot_encoder(data, ['Pclass', 'Sex', 'Cabin', 'Embarked'])


def one_hot_encode(x_train, x_valid):
    encoder = create_one_hot_encoder(x_train)
    x_train = encoder.transform(x_train)
    x_valid = encoder.transform(x_valid)
    return [x_train, x_valid]


def drop_non_numeric_columns(x_train, x_valid):
    x_train = drop_non_numeric(x_train)
    x_valid = drop_non_numeric(x_valid)
    return [x_train, x_valid]


def get_metrics(model, inputs, targets, data_set_name):
    targets_predications, score = get_metrics_internal(
        model, inputs, targets)
    targets['PredictedSurvived'] = targets_predications
    targets['Type'] = 'Training'

    metric_prefix = str(data_set_name).lower()

    return [targets, score], {'{}_score'.format(metric_prefix): score, 'data_set_name': data_set_name}
