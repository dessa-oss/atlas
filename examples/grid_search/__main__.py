"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
Please have a look at the "logistic_regression" and "cache" modules before looking at this one.

There are three main things to look at: "Hyperparameter"s, "DiscreteHyperparameter"s, and .grid_search().

Hyperparameter:
    Typically, you'll have parameters that you'll want to vary across jobs while keeping
    the basic structure the same - e.g. learning rate, number of neurons in a fully-
    connected layer, etc.  By providing a Hyperparameter object in place of an actual value,
    you create a hole that can be filled during invocation of .run() - or more importantly,
    a hyperparameter search.  An example of which is...

.grid_search():
    When you call .run() on a stage, you can supply to it arguments with which to fill a
    hyperparameter-shaped hole.  Below, we could have run the "log" stage like so:
    log.run(C=0.25, max_iter=100).  This would be suitable for a single run.  You could then
    use nested for loops to iterate over a search space in a grid search, where you call log.run()
    multiple times.  That sounds like annoying boilerplate, and it is!  Foundations provides a
    .grid_search() method that automates this.  All you need to do is supply ranges that your
    hyperparameters may take.  Among other classes provided, you can do this with...

DiscreteHyperparameter:
    A DiscreteHyperparameter object represents a discrete iterable of values a hyperparameter may
    take.  It is essentially a list with an interface better tuned toward hyperparameter search.
    The constructor takes the list of allowed values.  There are other hyperparameter range objects
    too, such as FloatingHyperparameter, which represents a uniform distribution over a closed interval.

These three concepts work together to allow you to perform a hyperparameter search very efficiently!
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
    foundations.set_project_name('Titanic Survival')

    # data prep
    data = load_data().enable_caching()
    data = fill_categorical_nulls(data).enable_caching()

    # this line is dense, so step-by-step:
    #     1. before doing anything, check to see if this stage's output exists in cache
    #     2a. if it does, grab from cache
    #     2b. if it does not,
    #         * grab the output from fill_categorical_nulls
    #         * split inputs and targets
    #         * save these to cache
    #     3. the stage result is a list with two elements, so we split it into two elements (inputs, targets)
    inputs, targets = split_inputs_and_targets(data=data).enable_caching().split(2)

    # feature engineering
    x_train, x_valid, y_train, y_valid = split_training_and_validation(
        inputs=inputs, targets=targets).enable_caching().split(4)
    x_train, x_valid = impute(x_train=x_train, x_valid=x_valid).enable_caching().split(2)
    x_train, x_valid = one_hot_encode(x_train=x_train, x_valid=x_valid).enable_caching().split(2)
    x_train, x_valid = drop_non_numeric_columns(x_train=x_train, x_valid=x_valid).enable_caching().split(2)

    # model training and scoring
    params = {
        'C': foundations.Hyperparameter('C'),
        'max_iter': foundations.Hyperparameter('max_iter'),
    }

    model = train_logistic_regression(x_train, y_train, **params)
    y_train, train_score = get_metrics(model=model, inputs=x_train, targets=y_train, data_set_name='Training').split(2)
    y_valid, valid_score = get_metrics(model=model, inputs=x_valid, targets=y_valid, data_set_name='Validation').split(2)

    # print out the results
    log = log_formatted('\nTraining score was {}\nValidation score was {}', train_score, valid_score)

    params_ranges = {
        'C': foundations.DiscreteHyperparameter([0.25, 0.125, 1.0]),
        'max_iter': foundations.DiscreteHyperparameter([100, 200])
    }

    # the below line of code is equivalent to:
    #
    # for C in [0.25, 0.125, 1.0]:
    #     for max_iter in [100, 200]:
    #         log.run(C=C, max_iter=max_iter)
    #
    # Foundations automates this boilerplate away with the .grid_search() method
    log.grid_search(params_ranges)

if __name__ == '__main__':
    main()
