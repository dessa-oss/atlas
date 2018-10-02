"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
If you haven't seen the "replacing_nulls" or "one_hot_encode" modules yet, have a look
at one of those before you look at this one.

This is structured in much the same way as those other two modules, but there's a key
difference - there's a .split() method.  Due to the fact that Python is dynamically typed,
among other things, Foundations simply cannot know how many values a stage returns when
wrapping it.  You'll need to help just a little bit by calling the split method.

The usage is simple enough - do stage.split(n) if the stage wants to return n elements to
other stages.  See lines 36 - 40 in this file for examples of usage.
"""

import foundations
import config
from common.prep import union
from common.models import train_logistic_regression
from common.logging import log_formatted
from titanic.etl import load_data, fill_categorical_nulls, split_inputs_and_targets, split_training_and_validation, impute, one_hot_encode, drop_non_numeric_columns, get_metrics

union = foundations.create_stage(union)
train_logistic_regression = foundations.create_stage(train_logistic_regression)
log_formatted = foundations.create_stage(log_formatted)
load_data = foundations.create_stage(load_data)
fill_categorical_nulls = foundations.create_stage(fill_categorical_nulls)
split_inputs_and_targets = foundations.create_stage(split_inputs_and_targets)
split_training_and_validation = foundations.create_stage(split_training_and_validation)
impute = foundations.create_stage(impute)
one_hot_encode = foundations.create_stage(one_hot_encode)
drop_non_numeric_columns = foundations.create_stage(drop_non_numeric_columns)
get_metrics = foundations.create_stage(get_metrics)


def main():
    # set the project name
    foundations.set_project_name('lou')

    # data prep
    data = load_data()
    data = fill_categorical_nulls(data=data)
    inputs, targets = split_inputs_and_targets(data=data).split(2)

    # feature engineering
    x_train, x_valid, y_train, y_valid = split_training_and_validation(
        inputs=inputs, targets=targets).split(4)
    x_train, x_valid = impute(x_train=x_train, x_valid=x_valid).split(2)
    x_train, x_valid = one_hot_encode(x_train=x_train, x_valid=x_valid).split(2)
    x_train, x_valid = drop_non_numeric_columns(x_train=x_train, x_valid=x_valid).split(2)

    # model training and scoring
    model = train_logistic_regression(x_train=x_train, y_train=y_train)
    y_train, train_score = get_metrics(model=model, inputs=x_train, targets=y_train, data_set_name='Training').split(2)
    y_valid, valid_score = get_metrics(model=model, inputs=x_valid, targets=y_valid, data_set_name='Validation').split(2)
    results = union(first=y_train, second=y_valid)

    # print out the results
    log_formatted('\nData: {}\nTraining score was {}\nValidation score was {}',
                  results, train_score, valid_score).run()


if __name__ == '__main__':
    main()
