"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from sklearn.linear_model import LogisticRegression

def train_logistic_regression(x_train, y_train):
    model = LogisticRegression()
    model = model.fit(x_train, y_train)

    return model

def get_metrics(model, x_values, y_values):
    score = model.score(x_values, y_values)
    y_valid_predications = model.predict(x_values)
    return [y_valid_predications, score], {'score': score}
