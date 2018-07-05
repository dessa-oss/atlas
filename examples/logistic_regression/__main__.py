"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import vcat
import config
from staged_common.data import load_titanic
from staged_common.prep import get_mode, fillna, one_hot_encode, encode, assign_columns, union, train_imputer, train_one_hot_encoder, drop_non_numeric
from staged_common.models import train_logistic_regression, get_metrics
from staged_sklearn.model_selection import train_test_split
from staged_common.one_hot_encoder import OneHotEncoder
from staged_sklearn.preprocessing import Imputer
from staged_common.logging import log_data, log_formatted

def main():
    # load the data set
    data = load_titanic()

    # replace null category values with real ones
    data = fillna(data, 'Cabin', 'NULLCABIN')
    data = fillna(data, 'Embarked', 'NULLEMBARKED')

    # input/target split
    inputs = data[['Age', 'SibSp', 'Parch', 'Fare',
                   'Pclass', 'Sex', 'Cabin', 'Embarked']]
    targets = data[['Survived']]

    # train/validation split
    x_train, x_valid, y_train, y_valid = train_test_split(
        inputs, targets, test_size=0.2, random_state=42, stratify=targets.as_matrix()).splice(4)

    # impute numeric columns using mean
    encoder = train_imputer(x_train, ['Age', 'Fare'])
    x_train = encoder.transform(x_train)
    x_valid = encoder.transform(x_valid)

    # one hot encode categorical columns
    encoder = train_one_hot_encoder(x_train, ['Pclass', 'Sex', 'Cabin', 'Embarked'])
    x_train = encoder.transform(x_train)
    x_valid = encoder.transform(x_valid)

    # remove non numerical columns
    x_train = drop_non_numeric(x_train)
    x_valid = drop_non_numeric(x_valid)

    # train the model
    model = train_logistic_regression(x_train, y_train)

    # retrieve training predictions and metrics
    y_train_predications, train_score = get_metrics(model, x_train, y_train).splice(2)
    y_train = assign_columns(y_train, 'PredictedSurvived', y_train_predications)
    y_train = assign_columns(y_train, 'Type', 'Training')

    # retrieve validation predictions and metrics
    y_valid_predications, valid_score = get_metrics(model, x_valid, y_valid).splice(2)
    y_valid = assign_columns(y_valid, 'PredictedSurvived', y_valid_predications)
    y_train = assign_columns(y_valid, 'Type', 'Validation')

    results = union(y_train, y_valid)

    # print out the results
    log_formatted('\nData: {}\nTraining score was {}\nValidation score was {}', results, train_score, valid_score).run_same_process()

if __name__ == '__main__':
    main()