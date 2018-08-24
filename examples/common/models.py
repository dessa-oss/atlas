"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
This file contains code used in model training for logistic regression model.
In the Foundations framework, code is expected to be structured into stages - instead
of a monolithic code block, you have functions which represent stages in a job.

Something very important to note: there is no usage of the Foundations library itself
in this file.  The main thing that you need to do is simply structure your code
as composable functions.

The signature of such a function is as follows:
    - arguments are unrestricted - there can be as many as you want, in any order
    - it should return as its first value the object to pass to the next stage
    - if you want to pass multiple items to the next stage, or return multiple items,
        explicitly return a list (see "get_metrics_internal" below)
    - if logging is to be done, the item to be logged (a metric for example) should be 
        stored in a dict with some key, and the dict should be returned as a second
        return value (see "get_metrics" below)
"""

from sklearn.linear_model import LogisticRegression
import foundations

def train_logistic_regression(x_train, y_train, *logistic_regression_args, **logistic_regression_kwargs):
    model = LogisticRegression(*logistic_regression_args, **logistic_regression_kwargs)
    model = model.fit(x_train, y_train)

    return model

def get_metrics_internal(model, x_values, y_values):
    score = model.score(x_values, y_values)
    y_valid_predications = model.predict(x_values)
    return y_valid_predications, score

def get_metrics(model, x_values, y_values):
    y_valid_predications, score = get_metrics_internal(model, x_values, y_values)
    foundations.log_metric('score', score)
    return y_valid_predications, score
